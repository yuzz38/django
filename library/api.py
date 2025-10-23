from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
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
    def get_queryset(self):
        qs = super().get_queryset()
        
        if self.request.user.is_superuser:
            return qs
        
        if self.request.user.is_authenticated:
            return qs.filter(user=self.request.user)
        
        return Reader.objects.none()

class BookInstanceViewSet(mixins.ListModelMixin, 
                         mixins.CreateModelMixin, 
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         GenericViewSet):
    queryset = BookInstance.objects.all()
    serializer_class = BookInstanceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['borrower']  # Добавляем фильтр по borrower
    
    def get_queryset(self):
        qs = super().get_queryset()
        
        if self.request.user.is_superuser:
            return qs
        
        if self.request.user.is_authenticated:
            # Пользователь видит книги, которые он взял (где он borrower)
            try:
                reader = Reader.objects.get(user=self.request.user)
                return qs.filter(borrower=reader)
            except Reader.DoesNotExist:
                return BookInstance.objects.none()
        
        return BookInstance.objects.none()
    
    def perform_create(self, serializer):
        # При создании автоматически устанавливаем текущего пользователя как borrower
        if self.request.user.is_authenticated:
            try:
                reader = Reader.objects.get(user=self.request.user)
                serializer.save(borrower=reader)
            except Reader.DoesNotExist:
                serializer.save()