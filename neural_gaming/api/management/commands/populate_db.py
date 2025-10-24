from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.models import PCSetup, Game, GamePerformanceDataset, Prediction, Feedback
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **options):
        # Create sample user
        user, created = User.objects.get_or_create(
            username='sampleuser',
            defaults={'email': 'sample@example.com', 'first_name': 'Sample', 'last_name': 'User'}
        )
        if created:
            user.set_password('password123')
            user.save()
            self.stdout.write(self.style.SUCCESS('Created sample user'))

        # Create sample games
        games_data = [
            {'name': 'Cyberpunk 2077', 'genre': 'RPG', 'developer': 'CD Projekt Red', 'release_year': 2020, 'min_cpu': 'Intel Core i5-3570K', 'min_gpu': 'NVIDIA GeForce GTX 780', 'min_ram': 8},
            {'name': 'The Witcher 3', 'genre': 'RPG', 'developer': 'CD Projekt Red', 'release_year': 2015, 'min_cpu': 'Intel Core i5-2500K', 'min_gpu': 'NVIDIA GeForce GTX 660', 'min_ram': 6},
            {'name': 'Fortnite', 'genre': 'Battle Royale', 'developer': 'Epic Games', 'release_year': 2017, 'min_cpu': 'Intel Core i3-3225', 'min_gpu': 'Intel HD 4000', 'min_ram': 4},
        ]
        games = []
        for game_data in games_data:
            game, created = Game.objects.get_or_create(
                name=game_data['name'],
                defaults=game_data
            )
            games.append(game)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created game: {game.name}'))

        # Create sample PC setups
        setups_data = [
            {'user': user, 'cpu': 'Intel Core i7-10700K', 'gpu': 'NVIDIA RTX 3070', 'ram': 16, 'storage_type': 'SSD', 'cooling': 'Liquid', 'psu': '750W', 'created_at': timezone.now()},
            {'user': user, 'cpu': 'AMD Ryzen 5 5600X', 'gpu': 'NVIDIA RTX 3060', 'ram': 16, 'storage_type': 'SSD', 'cooling': 'Air', 'psu': '650W', 'created_at': timezone.now()},
        ]
        setups = []
        for setup_data in setups_data:
            setup, created = PCSetup.objects.get_or_create(
                user=setup_data['user'],
                cpu=setup_data['cpu'],
                gpu=setup_data['gpu'],
                defaults=setup_data
            )
            setups.append(setup)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created PC setup: {setup}'))

        # Create sample game performance datasets
        datasets_data = [
            {'cpu': 'Intel Core i7-10700K', 'gpu': 'NVIDIA RTX 3070', 'ram': 16, 'storage_type': 'SSD', 'game': games[0], 'fps': 60.5, 'cpu_usage': 75.2, 'gpu_usage': 85.1, 'temperature': 65.0},
            {'cpu': 'AMD Ryzen 5 5600X', 'gpu': 'NVIDIA RTX 3060', 'ram': 16, 'storage_type': 'SSD', 'game': games[1], 'fps': 90.3, 'cpu_usage': 60.8, 'gpu_usage': 70.5, 'temperature': 58.0},
            {'cpu': 'Intel Core i7-10700K', 'gpu': 'NVIDIA RTX 3070', 'ram': 16, 'storage_type': 'SSD', 'game': games[2], 'fps': 120.0, 'cpu_usage': 50.1, 'gpu_usage': 45.2, 'temperature': 55.0},
        ]
        for dataset_data in datasets_data:
            dataset, created = GamePerformanceDataset.objects.get_or_create(
                cpu=dataset_data['cpu'],
                gpu=dataset_data['gpu'],
                ram=dataset_data['ram'],
                storage_type=dataset_data['storage_type'],
                game=dataset_data['game'],
                defaults=dataset_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created performance dataset for {dataset.game.name}'))

        # Create sample predictions
        predictions_data = [
            {'setup': setups[0], 'game': games[0], 'predicted_fps': 62.0, 'predicted_cpu_usage': 78.0, 'predicted_gpu_usage': 88.0, 'predicted_temperature': 68.0},
            {'setup': setups[1], 'game': games[1], 'predicted_fps': 95.0, 'predicted_cpu_usage': 65.0, 'predicted_gpu_usage': 75.0, 'predicted_temperature': 60.0},
        ]
        predictions = []
        for pred_data in predictions_data:
            prediction, created = Prediction.objects.get_or_create(
                setup=pred_data['setup'],
                game=pred_data['game'],
                defaults=pred_data
            )
            predictions.append(prediction)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created prediction for {prediction.setup} playing {prediction.game.name}'))

        # Create sample feedback
        feedbacks_data = [
            {'user': user, 'setup': setups[0], 'game': games[0], 'prediction': predictions[0], 'actual_fps': 58.5, 'rating': 4, 'comments': 'Close prediction, but slightly lower FPS in reality.'},
            {'user': user, 'setup': setups[1], 'game': games[1], 'prediction': predictions[1], 'actual_fps': 92.0, 'rating': 5, 'comments': 'Very accurate prediction!'},
        ]
        for fb_data in feedbacks_data:
            feedback, created = Feedback.objects.get_or_create(
                user=fb_data['user'],
                setup=fb_data['setup'],
                game=fb_data['game'],
                prediction=fb_data['prediction'],
                defaults=fb_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created feedback by {feedback.user.username} for {feedback.game.name}'))

        self.stdout.write(self.style.SUCCESS('Sample data population completed!'))
