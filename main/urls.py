from . import views
from django.urls import path

app_name = 'dash'

urlpatterns = [
    path('', views.main, name = 'main'),
    #quiz create
    path('create-quizz', views.create_quiz, name = 'quiz_create'),
    path('create-question/<int:id>', views.create_question , name ='quest_create' ),
    #quiz & questions detials
    path('questions/<int:id>', views.questions_list, name = 'questions'),
    path('question-detail/<int:id>', views.quest_detail, name = 'quest_detail'),
    path('quiz-delete/<int:id>', views.quiz_delete , name ='quiz_delete' ),
    path('get-results/<int:id>', views.get_results , name ='get_results' ),
    path('result-detail/<int:id>', views.result_detail , name ='result_detail' ),
    path('add-question/<int:id>', views.add_question, name = 'add_question'),
    #auth
    path('login', views.logging_in, name = 'login'),
    path('register', views.register, name = 'register'),
]