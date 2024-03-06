
from django.shortcuts import render, redirect
from django.http import HttpResponse,Http404
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
    if quiz.is_active:
        questions = models.Question.objects.filter(
            quiz = quiz
        )
        context = {
            'quiz':quiz,
            'questions':questions
        }
        return render(request, 'front/quiz-detail.html', context)
    else:
        return HttpResponse("Quiz's time is over!")

from datetime import datetime

def quiz_edit(request, code):
    quiz = models.Quiz.objects.get(code=code)
    if request.method == 'POST':
        quiz.title = request.POST['title']
        starttime_str = request.POST['start_time']
        endtime_str = request.POST.get('end_time')
        quiz.starttime = datetime.strptime(starttime_str, '%Y-%m-%dT%H:%M') if starttime_str else None
        quiz.endtime = datetime.strptime(endtime_str, '%Y-%m-%dT%H:%M') if endtime_str else None
        quiz.save()
        return redirect('dash:main')
    return render(request, 'front/quiz-edit.html', {'quiz':quiz})

def create_answers(request, code):
    quiz = models.Quiz.objects.get(code=code)
    if quiz.is_active:
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
    else:
        return HttpResponse("Quiz's time is over!")
    return redirect('front:show_result', id=quiz_taker.id, code=code)

def show_result(request, id, code):
    quiz_taker = models.QuizTaker.objects.get(id=id)
    result = models.Result.objects.get(taker=quiz_taker, taker__quiz__code=code)
    context = {
        'quiz_taker':quiz_taker,
        'result':result,
        'percentage':(result.correct_answers/(result.correct_answers+result.incorrect_answers))*100,
    }
    return render(request, 'front/user-result.html', context)