from django.urls import path
from . import views

urlpatterns = [
    path('quiz-detail/<str:quiz_code>', views.quiz_detail, name='quiz-detail'),
    path('create-result/<str:quiz_code>', views.create_quiz_taker, name='create-quiz-taker'),
    ]
