from rest_framework import serializers
from .models import Feedback

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['usuario', 'comentario', 'nota']  # Ajuste os campos conforme necessário
