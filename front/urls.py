from django.urls import path
from . import views

app_name = 'front'

urlpatterns = [
    path('send/quiz/<str:code>', views.quiz_detail, name='quiz_detail'),
    path('create-answer/<str:code>/', views.create_answers, name='create_answers'),
    path('show-result/<int:id>/<str:code>/', views.show_result, name='show_result'),
    path('quiz-detail/<str:code>/', views.quiz_detail, name='quiz_detail'),
    path('quiz-edit/<str:code>/', views.quiz_edit, name='quiz_edit'),
]