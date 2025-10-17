from library.models import Author, Book, Genre, Reader, BookInstance
from django.views.generic import TemplateView

class ShowAuthorsView(TemplateView):
    template_name = "authors/show_authors.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['authors'] = Author.objects.all()
        context['genres'] = Genre.objects.all()
        context['books'] = Book.objects.all().prefetch_related('author', 'genres')
        context['readers'] = Reader.objects.all()
        context['bookinstances'] = BookInstance.objects.all().select_related('book', 'borrower')
        return context