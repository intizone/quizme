from django.urls import include, path
from . import views

app_name = 'api'

urlpatterns = [
    path('quiz-detail/<str:code>/', views.quiz_detail, name='quiz-detail'),
    path('quiz-edit/<str:code>/', views.quiz_edit, name='quiz-edit'),
    path('create-answers/<str:code>/', views.create_answers, name='create-answers'),
    path('show-result/<int:id>/<str:code>/', views.show_result, name='show-result'),
    path('create-quiz-taker/<int:quiz_id>/', views.create_quiz_taker, name='create-quiz-taker'),
    path('quiz-delete/<int:quiz_id>/', views.quiz_delete, name='quiz-delete'),
    path('get-results/<int:quiz_id>/', views.get_results, name='get-results'),
    path('result-detail/<int:result_id>/', views.result_detail, name='result-detail'),
    path('api-token-auth/', views.obtain_auth_token, name='api_token_auth'),
    path('create-question/<int:quiz_id>/', views.create_question, name='create-question'),
    path('create-option/<int:question_id>/', views.create_option, name='create-option'),
]
