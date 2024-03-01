from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from main import models
from .serializers import *

@api_view(['GET'])
def quiz_detail(request, quiz_code):
    try:
        quiz = models.Quiz.objects.get(code=quiz_code)
    except models.Quiz.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = QuizDetailSerializer(quiz)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_quiz_taker(request, quiz_code):
    try:
        quiz = models.Quiz.objects.get(code=quiz_code)
    except models.Quiz.DoesNotExist:
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