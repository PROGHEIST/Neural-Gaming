from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'pcsetups', views.PCSetupViewSet)
router.register(r'games', views.GameViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('feedback/', views.submit_feedback, name='submit_feedback'),
    path('predict/', views.predict_performance, name='predict_performance'),
]
