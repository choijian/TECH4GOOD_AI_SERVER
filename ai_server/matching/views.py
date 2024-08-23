import os
import json
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import UserInfo, UserEmbedding
from .serializers import UserInfoSerializer, EmbeddedSeniorProfileSerializer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# SentenceTransformer 모델 로드
model = SentenceTransformer('jhgan/ko-sroberta-multitask', device='cpu')

# 임베딩 생성 함수
def get_embedding(text):
    return model.encode(text).tolist()

# 코사인 유사도 계산 함수
def calculate_cosine_similarity(embedding1, embedding2):
    return cosine_similarity([embedding1], [embedding2])[0][0]

class SeniorRecommendView(APIView):

    def post(self, request, *args, **kwargs):
        # 현재 로그인한 사용자의 user_seq 받아오기
        user_seq = request.data.get('user_seq')
        user_profile = UserInfo.objects.get(user_seq=user_seq)
        user_profile_data = UserInfoSerializer(user_profile).data
                
        # 비교 값의 임베딩 계산
        embedded_user = {key: get_embedding(str(value)) for key, value in user_profile_data.items() if value}

        # 선배 프로필 데이터 가져오기
        embedded_senior_profiles = UserEmbedding.objects.all()
        embedded_senior_profiles_data = EmbeddedSeniorProfileSerializer(embedded_senior_profiles, many=True).data
        
        if request.data.get('concepts') == 1: # 직업 & 관심사 기반
            weights_str = os.getenv('WEIGHTS1', '{}')
            
        elif request.data.get('concepts') == 2: # 취미 & 성격 기반
            weights_str = os.getenv('WEIGHTS2', '{}')
            
        else: # 기본
            weights_str = os.getenv('WEIGHTS', '{}')
        
        weights = json.loads(weights_str)
        
        similarities = []

        for profile in embedded_senior_profiles_data:
            similarity_sum = 0
            
            for key, user_embedding in embedded_user.items():
                profile_embedding = profile.get(key + '_embedding')
                
                if profile_embedding:
                    # 유사도 합 계산시 가중치 반영(percentage로 변환)
                    similarity_sum += weights[key] * calculate_cosine_similarity(profile_embedding, user_embedding) * 100
                    
            similarities.append({
                "user_seq": profile["user_info"]["user_seq"],
                "similarity_sum": similarity_sum
            })

        # 유사도 합계에 따라 정렬
        top3_similar = sorted(similarities, key=lambda x: x["similarity_sum"], reverse=True)[:3]
        
        # 정수 부분만 포맷하고 % 기호 추가
        for item in top3_similar:
            item["similarity_sum"] = f"{int(item['similarity_sum'])}%"
            
        return Response(top3_similar, status=status.HTTP_200_OK)
    