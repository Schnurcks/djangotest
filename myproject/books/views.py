from django.shortcuts import render
from .models import Book, UserBook

def booklist(request):
  booklist = Book.objects.all()
  return render(request, 'books/booklist.html', {'books':booklist, 'section': 'booklist'})
