from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.
@login_required(login_url = 'dash:login')
def main(request):
    quizes = Quiz.objects.filter(author = request.user)
    context = {
        "quizes" : quizes
    }
    return render(request, 'main.html', context)

@login_required(login_url = 'dash:login')
def create_quiz(request):
    if request.method == 'POST':
        title = request.POST['title']
        quiz = Quiz.objects.create(
            title = title,
            author = request.user
        )
        return redirect('dash:quest_create', quiz.id)
    return render(request, 'quiz/create-quiz.html')

@login_required(login_url='dash:login')
def create_question(request, id):
    quiz = Quiz.objects.get(id=id)
    if request.method == 'POST':
        title = request.POST['title']
        ques = Question.objects.create(
            quiz=quiz,
            title=title
        )
        correct_answer = request.POST['correct']
        Option.objects.create(
            question=ques,
            name=correct_answer,
            is_correct=True
        )
        incorrect_answers = [request.POST[key] for key in request.POST if key.startswith('incorrect')]
        
        for incorrect_answer in incorrect_answers:
            Option.objects.create(
                question=ques,
                name=incorrect_answer,
                is_correct=False
            )
        if request.POST['submit_action'] == 'exit':
            return redirect('dash:main')
    return render(request, 'quiz/create-question.html')

@login_required(login_url = 'dash:login')
def questions_list(request, id):
    correct_answer = Option.objects.filter(question__quiz_id = id, is_correct = True)
    quests = Question.objects.filter(quiz_id = id)
    context = {
        'questions': quests,
        'correct_answer': correct_answer[0]
    }
    return render (request, 'details/questions.html', context)

@login_required(login_url='dash:login')
def quest_detail(request, id):
    question = Question.objects.get(id=id)
    option_correct = Option.objects.get(question=question, is_correct=True)
    options = Option.objects.filter(question=question, is_correct=False).order_by('id')
    context = {
        'question': question,
        'options': options,
        'option_correct': option_correct
    }
    if request.method == 'POST':
        question.title = request.POST['title']
        question.save()

        option_correct.name = request.POST['correct']
        option_correct.save()

        # Extract all incorrect answers dynamically
        incorrect_answers = []
        for key, value in request.POST.items():
            if key.startswith('incorrect'):
                incorrect_answers.append(value)

        for i, opt in enumerate(options):
            if i < len(incorrect_answers):
                opt.name = incorrect_answers[i]
                opt.save()

    return render(request, 'details/detail.html', context)

@login_required(login_url = 'dash:login')
def quiz_delete(request, id):
    Quiz.objects.get(id = id).delete()
    return redirect('dash:main')

@login_required(login_url = 'dash:login')
def add_question(request, id):
    quiz = Quiz.objects.get(id = id)
    if request.method == 'POST':
        title = request.POST['title']
        question = Question.objects.create(
            quiz = quiz,
            title = title
        )
        correct_answer = request.POST['correct']
        Option.objects.create(
            question = question,
            name = correct_answer,
            is_correct = True
        )
        incorrect_answers = [request.POST[key] for key in request.POST if key.startswith('incorrect')]
        for incorrect_answer in incorrect_answers:
            Option.objects.create(
                question = question,
                name = incorrect_answer,
                is_correct = False
            )
        if request.POST['submit_action'] == 'exit':
            return redirect('dash:main')
    return render(request, 'details/add-question.html')


@login_required(login_url = 'dash:login')
def quiz_delete(request, id):
    Quiz.objects.get(id = id).delete()
    return redirect('dash:main')

@login_required(login_url = 'dash:login')
def get_results(request, id):
    quiz = Quiz.objects.get(id=id)
    taker = QuizTaker.objects.filter(quiz=quiz)

    # results = []
    # for i in taker:
    #     results.append(Result.objects.get(taker=i))
    
    results = tuple(
            map(
            lambda x : Result.objects.get(taker=x),
            taker
        )
    )
    return render(request, 'quiz/results.html', {'results':results})

def result_detail(request, id):
    result = Result.objects.get(id=id)
    answers = Answer.objects.filter(taker=result.taker)
    context = {
        'taker':result.taker,
        'answers':answers
    }
    return render(request, 'quiz/result-detail.html', context)

#login


def logging_in(request):
    status = False
    if request.method == 'POST':
        username = request.POST['username']
        password =  request.POST['password']
        user = authenticate(username = username, password=password)
        if user:
            login(request, user)
            return redirect('dash:main')
        else:
            status = 'incorrect username or password'
    return render(request, 'auth/login.html', {'status':status})

def register(request):
    status = False
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if not User.objects.filter(username = username).first():
            User.objects.create_user(
                username=username,
                password=password
            )
            user = authenticate(username = username, password = password)
            login(request, user)
            return redirect('dash:main')
        else:
            status  = f'the username {username} is occupied'
    return render(request, 'auth/register.html', {'status': status})

