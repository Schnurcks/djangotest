from django.contrib import admin
from .models import Author, Genre, Book, UserBook

admin.site.register(Author)
admin.site.register(Genre)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author','display_genre')

@admin.register(UserBook)
class UserBookAdmin(admin.ModelAdmin):
    list_display = ('book', 'book_author', 'user', 'is_favorite', 'rating')

    def book_author(self, obj):
        return obj.book.author