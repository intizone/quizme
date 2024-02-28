
from django.shortcuts import render, redirect
from main import models


def quiz_detail(request, code):
    quiz = models.Quiz.objects.get(code=code)
    questions = models.Question.objects.filter(
        quiz = quiz
    )
    context = {
        'quiz':quiz,
        'questions':questions
    }
    return render(request, 'front/quiz-detail.html', context)


def create_answers(request, code):
    print(request.POST)