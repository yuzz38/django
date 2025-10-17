from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets
from library.models import Author, Book, Genre, Reader, BookInstance
from library.serializers import AuthorSerializer, BookSerializer, GenreSerializer, ReaderSerializer, BookInstanceSerializer

class AuthorViewSet(mixins.ListModelMixin, 
                   mixins.CreateModelMixin, 
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class GenreViewSet(mixins.ListModelMixin, 
                  mixins.CreateModelMixin, 
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class BookViewSet(mixins.ListModelMixin, 
                 mixins.CreateModelMixin, 
                 mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 GenericViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class ReaderViewSet(mixins.ListModelMixin, 
                   mixins.CreateModelMixin, 
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):
    queryset = Reader.objects.all()
    serializer_class = ReaderSerializer

class BookInstanceViewSet(mixins.ListModelMixin, 
                         mixins.CreateModelMixin, 
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         GenericViewSet):
    queryset = BookInstance.objects.all()
    serializer_class = BookInstanceSerializer