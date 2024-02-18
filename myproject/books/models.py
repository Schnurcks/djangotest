from django.db import models
from django.contrib.auth.models import User

from django.core.exceptions import ValidationError

def validate_svg(file):
    if not file.name.lower().endswith('.svg'):
        raise ValidationError("Only SVG-Files are allowed.")

class Genre(models.Model):
  name = models.CharField(
    max_length=200,
    unique=True,
    help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)"
    )

  def __str__(self):
    return self.name


class Author(models.Model):
  # TODO Add countries here
  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)

  class Meta:
    ordering = ['last_name', 'first_name']

  def __str__(self):
    return f'{self.last_name}, {self.first_name}'


class Book(models.Model):
  title = models.CharField(max_length=200)
  author = models.ForeignKey('Author', on_delete=models.RESTRICT, null=True)
  genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
  cover = models.FileField(upload_to='books/%Y/%m/%d/', blank=True, validators=[validate_svg])

  class Meta:
    ordering = ['title', 'author']

  def display_genre(self):
    """Creates a string for the Genre. This is required to display genre in Admin."""
    return ', '.join([genre.name for genre in self.genre.all()[:3]])

  display_genre.short_description = 'Genre'

  def __str__(self):
    return self.title

  
class UserBook(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  book = models.ForeignKey(Book, on_delete=models.CASCADE)

  is_favorite = models.BooleanField(default=False)

  rating_choices = (
        (1, '1*'),
        (2, '2*'),
        (3, '3*'),
        (4, '4*'),
        (5, '5*'),
    )
  
  rating = models.IntegerField(choices=rating_choices, null=True)

  def __str__(self):
    return f'{self.book} ({self.user})'
