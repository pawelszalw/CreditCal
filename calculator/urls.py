from django.urls import path
from . import views


urlpatterns = [
    path('', views.calculate_credit, name='calculate_credit'),
    path('about/', views.about, name='about'),  # Ścieżka do widoku "about"
]