from django.contrib import admin
from .models import Author, Book, Genre, Reader, BookInstance

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['nameAuthor', 'bio']

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['name', 'author','publication_year']
    list_filter = ['genres']

@admin.register(Reader)
class ReaderAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'card_number']

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ['book', 'status', 'due_back', 'borrower']
    list_filter = ['status', 'due_back']