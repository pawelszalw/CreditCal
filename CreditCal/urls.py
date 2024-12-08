from django.contrib import admin
from django.urls import path
from calculator import views  # Import your views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Home page
    path('new-loan/', views.new_loan, name='new_loan'),  # New Loan page
    path('my-loan/', views.my_loan, name='my_loan'),  # New Loan page
    path('overpayment/', views.overpayment, name='overpayment'),  # Overpayment page
    path('about/', views.about, name='about'),  # About page
]
