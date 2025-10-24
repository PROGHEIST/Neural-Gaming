from django.db import models
from django.contrib.auth.models import User

class PCSetup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    cpu = models.CharField(max_length=100)
    gpu = models.CharField(max_length=100)
    ram = models.IntegerField()  # in GB
    storage_type = models.CharField(max_length=50)  # e.g., SSD, HDD
    cooling = models.CharField(max_length=100, blank=True, null=True)
    psu = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.cpu} + {self.gpu}"

class Game(models.Model):
    name = models.CharField(max_length=100)
    genre = models.CharField(max_length=50, blank=True, null=True)
    developer = models.CharField(max_length=100, blank=True, null=True)
    release_year = models.IntegerField(blank=True, null=True)
    min_cpu = models.CharField(max_length=100, blank=True, null=True)
    min_gpu = models.CharField(max_length=100, blank=True, null=True)
    min_ram = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

class GamePerformanceDataset(models.Model):
    cpu = models.CharField(max_length=100)
    gpu = models.CharField(max_length=100)
    ram = models.IntegerField()
    storage_type = models.CharField(max_length=50)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    fps = models.FloatField()
    cpu_usage = models.FloatField()
    gpu_usage = models.FloatField()
    temperature = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dataset for {self.game.name}"

class Prediction(models.Model):
    setup = models.ForeignKey(PCSetup, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    predicted_fps = models.FloatField()
    predicted_cpu_usage = models.FloatField()
    predicted_gpu_usage = models.FloatField()
    predicted_temperature = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prediction for {self.setup} playing {self.game.name}"

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    setup = models.ForeignKey(PCSetup, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    prediction = models.ForeignKey(Prediction, on_delete=models.CASCADE, null=True, blank=True)
    actual_fps = models.FloatField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5
    comments = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.user.username} for {self.game.name}"
