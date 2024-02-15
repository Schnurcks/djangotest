from django.urls import path, include
from .forms import AuthenticationFormWCaseInsensitive
from django.contrib.auth.views import LoginView

from . import views

urlpatterns = [
    path('login/', LoginView.as_view(template_name='registration/login.html', authentication_form=AuthenticationFormWCaseInsensitive), name='login'),
    path('', include('django.contrib.auth.urls')),
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('activationlink/', views.resent_activation, name='resent_activation')
]
