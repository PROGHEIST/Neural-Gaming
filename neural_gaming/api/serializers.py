from rest_framework import serializers
from .models import PCSetup, Game, Feedback

class PCSetupSerializer(serializers.ModelSerializer):
    class Meta:
        model = PCSetup
        fields = '__all__'

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'
