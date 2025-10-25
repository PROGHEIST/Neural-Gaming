from django.db import models

class UserProfile(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class CPU(models.Model):
    name = models.CharField(max_length=100)
    cores = models.IntegerField()
    threads = models.IntegerField()
    base_clock = models.FloatField() 
    boost_clock = models.FloatField()
    tdp = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name
    
class GPU(models.Model):
    name = models.CharField(max_length=100)
    vram = models.IntegerField()  # in GB
    base_clock = models.FloatField()
    boost_clock = models.FloatField()
    tdp = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name

class RAM(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()  # in GB
    speed = models.IntegerField()  # in MHz
    type = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name

class Storage(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()  # in GB
    type = models.CharField(max_length=50)  # e.g., SSD, HDD
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name

class Motherboard(models.Model):
    name = models.CharField(max_length=100)
    chipset = models.CharField(max_length=100)
    form_factor = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name

class PowerSupply(models.Model):
    name = models.CharField(max_length=100)
    wattage = models.IntegerField()  # in Watts
    efficiency_rating = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name

class ComputerBuild(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    cpu = models.ForeignKey(CPU, on_delete=models.CASCADE)
    gpu = models.ForeignKey(GPU, on_delete=models.CASCADE)
    ram = models.ForeignKey(RAM, on_delete=models.CASCADE)
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)
    motherboard = models.ForeignKey(Motherboard, on_delete=models.CASCADE)
    power_supply = models.ForeignKey(PowerSupply, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Build by {self.user.username} on {self.created_at.strftime('%Y-%m-%d')}"

class GameBenchmark(models.Model):
    build = models.ForeignKey(ComputerBuild, on_delete=models.CASCADE)
    game_name = models.CharField(max_length=100)
    average_fps = models.FloatField()
    resolution = models.CharField(max_length=50)
    settings = models.CharField(max_length=100)
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.game_name} Benchmark for {self.build}"
    
class PerformanceMetric(models.Model):
    build = models.ForeignKey(ComputerBuild, on_delete=models.CASCADE)
    cpu_usage = models.FloatField()  # in percentage
    gpu_usage = models.FloatField()  # in percentage
    ram_usage = models.FloatField()  # in percentage
    temperature = models.FloatField()  # in Celsius
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Performance Metric for {self.build} at {self.recorded_at.strftime('%Y-%m-%d %H:%M:%S')}"