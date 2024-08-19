import os
import boto3
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser

def get_embeddings():
    return OpenAIEmbeddings(model="text-embedding-3-small")

def load_vectorstore():
    db_path = os.path.join(settings.STATICFILES_DIRS[0]) # 데이터베이스 경로 설정
    embeddings = get_embeddings()
    vectorstore = FAISS.load_local(db_path, embeddings, allow_dangerous_deserialization=True) # FAISS 인덱스 로드
    
    return vectorstore

def format_docs(docs):
    return '\n\n'.join([d.page_content for d in docs])

class ChatbotView(APIView):
    def post(self, request, *args, **kwargs):
        question = request.data.get("question")
        
        # model
        llm = ChatOpenAI(model='gpt-3.5-turbo-0125', temperature=0, max_tokens=500)
        
        # prompt
        template = """
            당신은 자립청소년의 질문에 대한 답변을 제공하는 어시스턴트입니다.
            다음의 검색된 문서에서 제공된 정보를 사용하여 질문에 답변하세요.
            답을 모를 경우, 모른다고 말하세요.
            답변은 한국어로 작성하세요.
            검색된 문서에 근거하여 답변하세요.
            관련된 하나 은행의 금융 상품 또는 정책이 있으면 자세하게 같이 설명해주세요.
            
            {question}
        """

        prompt = ChatPromptTemplate.from_template(template)
        
        # vectorDB
        vectorstore = load_vectorstore()
        retriever = vectorstore.as_retriever(search_kwargs={'k': 5})

        #Chain
        chain = prompt | llm | StrOutputParser()
            
        vectorstore = load_vectorstore()
        retriever = vectorstore.as_retriever(search_kwargs={'k': 5})
        
        docs = retriever.invoke(question)
        
        # Run
        answer = chain.invoke({'context': (format_docs(docs)), 'question':question})
        
        response_data = {
            "answer": answer
        }
        
        return Response(response_data, status=status.HTTP_200_OK)