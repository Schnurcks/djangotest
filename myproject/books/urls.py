from django.urls import path
from . import views

urlpatterns = [
    path('', views.booklist, name='booklist'),
]
