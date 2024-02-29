
from django.shortcuts import render, redirect
from django.http import HttpResponse
from main import models

def create_result(id):
    quiz_taker = models.QuizTaker.objects.get(id=id)
    correct = 0
    incorrect = 0
    for object in models.Answer.objects.filter(taker=quiz_taker):
        if object.is_correct:
            correct +=1
        else:
            incorrect +=1

    models.Result.objects.create(
        taker=quiz_taker,
        correct_answers=correct,
        incorrect_answers=incorrect
    )

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
    quiz = models.Quiz.objects.get(code=code)
    full_name = request.POST['full_name']
    phone = request.POST['phone']
    email = request.POST.get('email')
    quiz_taker = models.QuizTaker.objects.create(
        full_name=full_name,
        phone=phone,
        email=email,
        quiz=quiz
    )
    for key, value in request.POST.items():
        if key.isdigit():
            models.Answer.objects.create(
                taker=quiz_taker,
                question_id=int(key),
                answer_id=int(value),
                is_correct=models.Option.objects.get(id=int(value)).is_correct

            )
    create_result(quiz_taker.id)
    return HttpResponse('Javobingiz yozildi')