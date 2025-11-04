from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
from django.db.models import Avg, Count, Max, Min
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
    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg_books = serializers.FloatField()
        max_books = serializers.IntegerField()
        min_books = serializers.IntegerField()
        total_books = serializers.IntegerField()
        
    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, request, *args, **kwargs):

      
        
        
        total_authors = Author.objects.count()
        
    
        author_stats = Author.objects.annotate(
            book_count=Count('book') 
        ).aggregate(
            count=Count("*"),
            avg_books=Avg("book_count"),
            max_books=Max("book_count"),
            min_books=Min("book_count"),
        )
        
    
        total_books = Book.objects.count()
     
        stats = {
            'count': total_authors,
            'avg_books': author_stats['avg_books'],
            'max_books': author_stats['max_books'],
            'min_books': author_stats['min_books'],
            'total_books': total_books
        }
        
        serializer = self.StatsSerializer(instance=stats)
        return Response(serializer.data)

   

class GenreViewSet(mixins.ListModelMixin, 
                  mixins.CreateModelMixin, 
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    class GenreStatsSerializer(serializers.Serializer):
        total_genres = serializers.IntegerField()
        total_books = serializers.IntegerField()
        
        most_popular_genre = serializers.CharField()
        books_in_popular_genre = serializers.IntegerField()
        
    @action(detail=False, methods=["GET"], url_path="stats")
    def get_genre_stats(self, request, *args, **kwargs):
     
        
        
        genre_stats = Genre.objects.annotate(
            book_count=Count('book')  
        ).order_by('-book_count')
        
        total_genres = genre_stats.count()
        total_books = Book.objects.count()
        
        
        most_popular = genre_stats.first()
        
        stats = {
            'total_genres': total_genres,
            'total_books': total_books,
            'most_popular_genre': most_popular.name,
            'books_in_popular_genre': most_popular.book_count
        }
        
        serializer = self.GenreStatsSerializer(instance=stats)
        return Response(serializer.data)
    

class BookViewSet(mixins.ListModelMixin, 
                 mixins.CreateModelMixin, 
                 mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 GenericViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    class BookStatsSerializer(serializers.Serializer):
        total_books = serializers.IntegerField()
        avg_publication_year = serializers.FloatField()
        oldest_book_year = serializers.IntegerField()
        newest_book_year = serializers.IntegerField()
        most_popular_author = serializers.CharField()
        books_by_popular_author = serializers.IntegerField()
  
        
    @action(detail=False, methods=["GET"], url_path="stats")
    def get_book_stats(self, request, *args, **kwargs):
        # Статистика по книгам
        book_stats = Book.objects.aggregate(
            total_books=Count("*"),
            avg_publication_year=Avg("publication_year"),
            oldest_book_year=Min("publication_year"),
            newest_book_year=Max("publication_year"),
        )
        
        # Статистика по авторам
        author_stats = Author.objects.annotate(
            book_count=Count('book')
        ).order_by('-book_count').first()
        
  
        
        stats = {
            'total_books': book_stats['total_books'],
            'avg_publication_year': round(book_stats['avg_publication_year'], 1),
            'oldest_book_year': book_stats['oldest_book_year'],
            'newest_book_year': book_stats['newest_book_year'],
            'most_popular_author': author_stats.nameAuthor,
            'books_by_popular_author': author_stats.book_count,
           
        }
        
        serializer = self.BookStatsSerializer(instance=stats)
        return Response(serializer.data)
  
class UserViewSet(viewsets.GenericViewSet):
    permission_classes = []

    @action(detail=False, url_path="info", methods=["GET"])
    def get_info(self, request, *args, **kwargs):
        return Response({
            "username": request.user.username,
            "is_authenticated": request.user.is_authenticated,
           
            "is_staff": request.user.is_staff,
        })

    @action(detail=False, url_path="login", methods=["POST"])
    def login_user(self, request, *args, **kwargs):
        username = self.request.data['username']
        password = self.request.data['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)

            return Response({
                'success': True,
            })

        return Response({
            'success': False,
        })
    @action(detail=False, url_path="logout", methods=["POST"])
    def logout_user(self, request, *args, **kwargs):
        logout(request)
        return Response({
            'success': True,
        }, status=status.HTTP_200_OK)
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