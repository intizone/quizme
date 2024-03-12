
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from requests import Response
from rest_framework import status

from main.models import Quiz, QuizTaker, Result, Answer, Question, Option
from .serializers import (QuizSerializer, QuizTakerSerializer, 
                          ResultSerializer, AnswerSerializer, 
                          QuestionSerializer, OptionSerializer)


@api_view(['GET'])
def quiz_detail(request, quiz_id):
    try:
        quiz = Quiz.objects.get(id=quiz_id)
        serializer = QuizSerializer(quiz)
        return Response(serializer.data)
    except Quiz.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def create_quiz_taker(request, quiz_id):
    try:
        quiz = Quiz.objects.get(id=quiz_id)
    except Quiz.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
        
    serializer = QuizTakerSerializer(data=request.data)
    if serializer.is_valid():
        quiz_taker = serializer.save(quiz=quiz)
        answers_data = request.data.get('answers', [])
        for answer_data in answers_data:
            answer_data['quiz_taker'] = quiz_taker.id
            answer_serializer = AnswerSerializer(data=answer_data)
            if answer_serializer.is_valid():
                answer_serializer.save()
            else:
                return Response(answer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
def quiz_delete(request, quiz_id):
    try:
        quiz = Quiz.objects.get(id=quiz_id)
        quiz.delete()
    except Quiz.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def get_results(request, quiz_id):
    try:
        quiz = Quiz.objects.get(id=quiz_id)
    except Quiz.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    takers = QuizTaker.objects.filter(quiz=quiz)
    results = []
    for taker in takers:
        result = Result.objects.filter(taker=taker).first()
        if result:
            results.append(result)
    
    serializer = ResultSerializer(results, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def result_detail(request, result_id):
    try:
        result = Result.objects.get(id=result_id)
    except Result.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    answers = Answer.objects.filter(taker=result.taker)
    serializer = AnswerSerializer(answers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    serializer = QuestionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(quiz=quiz)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_option(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    serializer = OptionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(question=question)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def quiz_detail(request, code):
    quiz = get_object_or_404(Quiz, code=code)
    if quiz.is_active:
        serializer = QuizSerializer(quiz)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response("Quiz's time is over!", status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def quiz_edit(request, code):
    quiz = get_object_or_404(Quiz, code=code)
    if request.method == 'PUT':
        serializer = QuizSerializer(quiz, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_answers(request, code):
    quiz = get_object_or_404(Quiz, code=code)
    if quiz.is_active:
        serializer = QuizTakerSerializer(data=request.data)
        if serializer.is_valid():
            quiz_taker = serializer.save(quiz=quiz)
            answers_data = request.data.get('answers', [])
            correct = 0
            incorrect = 0
            for answer_data in answers_data:
                answer_data['quiz_taker'] = quiz_taker.id
                answer_serializer = AnswerSerializer(data=answer_data)
                if answer_serializer.is_valid():
                    answer = answer_serializer.save()
                    if answer.is_correct:
                        correct += 1
                    else:
                        incorrect += 1
                else:
                    return Response(answer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            Result.objects.create(taker=quiz_taker, correct_answers=correct, incorrect_answers=incorrect)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("Quiz's time is over!", status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def show_result(request, id, code):
    quiz_taker = get_object_or_404(QuizTaker, id=id)
    result = get_object_or_404(Result, taker=quiz_taker, taker__quiz__code=code)
    serializer = ResultSerializer(result)
    return Response(serializer.data, status=status.HTTP_200_OK)


