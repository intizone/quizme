from main.models import Quiz, QuizTaker, Result, Answer, Question, Option
from rest_framework import serializers


# main
class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'author', 'starttime', 'endtime']

class QuizTakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizTaker
        fields = ['id', 'user', 'quiz', 'completed']

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ['id', 'taker', 'quiz', 'score', 'percentage']

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'taker', 'question', 'option', 'is_correct']

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'quiz', 'title']

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'question', 'name', 'is_correct']



# front
class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'code', 'is_active', 'starttime', 'endtime']

class QuizTakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizTaker
        fields = ['id', 'full_name', 'phone', 'email', 'quiz']

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ['id', 'taker', 'correct_answers', 'incorrect_answers']

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'taker', 'question', 'answer', 'is_correct']

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'quiz', 'text']

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'question', 'text', 'is_correct']


# from main import models
# from rest_framework import serializers


# class QuizDetailSerializer(serializers.ModelSerializer):
#     questions = serializers.SerializerMethodField()

#     class Meta:
#         model = models.Quiz
#         fields = '__all__'

#     def get_questions(self, obj):
#         questions = models.Question.objects.filter(quiz=obj)
#         return QuestionSerializer(questions, many=True).data


# class OptionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Option
#         fields = '__all__'


# class AnswerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Answer
#         fields = '__all__'


# class QuestionSerializer(serializers.ModelSerializer):
#     options = OptionSerializer(many=True, read_only=True)
#     answers = AnswerSerializer(many=True, read_only=True)

#     class Meta:
#         model = models.Question
#         fields = '__all__'

# class QuizTakerSerializer(serializers.ModelSerializer):
#     answers = AnswerSerializer(many=True)

#     class Meta:
#         model = models.QuizTaker
#         fields = '__all__'
#         read_only_fields = ('quiz',)

#     def create(self, validated_data):
#         answers_data = validated_data.pop('answers')
#         quiz_taker = models.QuizTaker.objects.create(**validated_data)
#         for answer_data in answers_data:
#             answer_data['taker'] = quiz_taker
#             AnswerSerializer().create(answer_data)
#         return quiz_taker
