from django.urls import path
from . import views


# Home page
def home(request):
    return render(request, 'calculator/home.html')

urlpatterns = [
    path('', views.calculate_credit, name='calculate_credit'),
    path('about/', views.about, name='about'),  # Ścieżka do widoku "about"
]