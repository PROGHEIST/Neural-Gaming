from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import PCSetup, Game, Feedback, Prediction, GamePerformanceDataset
from .serializers import PCSetupSerializer, GameSerializer, FeedbackSerializer, PredictionSerializer
from django.db.models import Avg

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
    setup_id = request.query_params.get('setup_id')
    game_id = request.query_params.get('game_id')
    if not setup_id or not game_id:
        return Response({'error': 'setup_id and game_id are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        setup = PCSetup.objects.get(id=setup_id)
        game = Game.objects.get(id=game_id)
    except PCSetup.DoesNotExist:
        return Response({'error': 'PCSetup not found'}, status=status.HTTP_404_NOT_FOUND)
    except Game.DoesNotExist:
        return Response({'error': 'Game not found'}, status=status.HTTP_404_NOT_FOUND)

    # Try to find exact matches in GamePerformanceDataset
    exact_matches = GamePerformanceDataset.objects.filter(
        cpu=setup.cpu,
        gpu=setup.gpu,
        ram=setup.ram,
        storage_type=setup.storage_type,
        game=game
    )

    if exact_matches.exists():
        # Average the exact matches
        avg_data = exact_matches.aggregate(
            avg_fps=Avg('fps'),
            avg_cpu_usage=Avg('cpu_usage'),
            avg_gpu_usage=Avg('gpu_usage'),
            avg_temperature=Avg('temperature')
        )
    else:
        # Fallback to average all datasets for the game
        game_datasets = GamePerformanceDataset.objects.filter(game=game)
        if game_datasets.exists():
            avg_data = game_datasets.aggregate(
                avg_fps=Avg('fps'),
                avg_cpu_usage=Avg('cpu_usage'),
                avg_gpu_usage=Avg('gpu_usage'),
                avg_temperature=Avg('temperature')
            )
        else:
            # No data available, return default values
            avg_data = {
                'avg_fps': 60.0,
                'avg_cpu_usage': 70.0,
                'avg_gpu_usage': 80.0,
                'avg_temperature': 65.0
            }

    # Create and save the prediction
    prediction = Prediction.objects.create(
        setup=setup,
        game=game,
        predicted_fps=avg_data['avg_fps'],
        predicted_cpu_usage=avg_data['avg_cpu_usage'],
        predicted_gpu_usage=avg_data['avg_gpu_usage'],
        predicted_temperature=avg_data['avg_temperature']
    )

    serializer = PredictionSerializer(prediction)
    return Response(serializer.data)
