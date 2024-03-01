from main import models
from rest_framework import serializers


class QuizDetailSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    class Meta:
        model = models.Quiz
        fields = '__all__'

    def get_questions(self, obj):
        questions = models.Question.objects.filter(quiz=obj)
        return QuestionSerializer(questions, many=True).data


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Option
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = models.Question
        fields = '__all__'

class QuizTakerSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = models.QuizTaker
        fields = '__all__'
        read_only_fields = ('quiz',)

    def create(self, validated_data):
        answers_data = validated_data.pop('answers')
        quiz_taker = models.QuizTaker.objects.create(**validated_data)
        for answer_data in answers_data:
            answer_data['taker'] = quiz_taker
            AnswerSerializer().create(answer_data)
        return quiz_taker
    

# {
#     "full_name": "palonchi",
#     "phone": "1234567890",
#     "answers": [
#         {
#             "question": 1,
#             "answer": 2,
#             "is_correct": true
#         },
#         {
#             "question": 2,
#             "answer": 3,
#             "is_correct": false
#         }
#     ]
# }