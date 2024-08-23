from django.urls import path
from .views import SeniorRecommendView

urlpatterns = [
    path('senior/', SeniorRecommendView.as_view(), name='similarity'),
]
