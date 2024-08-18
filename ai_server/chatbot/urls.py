from django.urls import path
from .views import ChatbotView

urlpatterns = [
    path('ai-answer/', ChatbotView.as_view(), name='chatbot'),
]