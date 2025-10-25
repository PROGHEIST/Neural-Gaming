from django.contrib import admin
from .models import UserProfile, CPU, GPU, RAM, Storage, Motherboard, PowerSupply

admin.site.register(UserProfile)
admin.site.register(CPU)
admin.site.register(GPU)
admin.site.register(RAM)  
admin.site.register(Storage)
admin.site.register(Motherboard)
admin.site.register(PowerSupply)