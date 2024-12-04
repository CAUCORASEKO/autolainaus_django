# lainaus_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Ruta para la página principal
    path('lainaus/', views.lainaus_view, name='lainaus'),  # Ruta para 'lainaus'
    path('palautus/', views.palautus_view, name='palautus'),  # Ruta para 'palautus'
    path('hallinto/', views.hallinto_view, name='hallinto'),  # Ruta para 'hallinto' (asegúrate de tener esta vista definida)
]
