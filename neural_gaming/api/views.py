from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import PCSetup, Game, Feedback
from .serializers import PCSetupSerializer, GameSerializer, FeedbackSerializer

class PCSetupViewSet(viewsets.ModelViewSet):
    queryset = PCSetup.objects.all()
    serializer_class = PCSetupSerializer

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

@api_view(['POST'])
def submit_feedback(request):
    serializer = FeedbackSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def predict_performance(request):
    # Dummy prediction logic
    setup_id = request.query_params.get('setup_id')
    game_id = request.query_params.get('game_id')
    if not setup_id or not game_id:
        return Response({'error': 'setup_id and game_id are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Dummy values
    predicted_fps = 60.0
    cpu_usage = 70.0
    gpu_usage = 80.0
    temperature = 65.0
    
    return Response({
        'predicted_fps': predicted_fps,
        'cpu_usage': cpu_usage,
        'gpu_usage': gpu_usage,
        'temperature': temperature
    })
