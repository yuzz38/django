from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
import io
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
import random
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
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsDoubleFAVerified()]
        return [permissions.IsAuthenticated()]
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
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsDoubleFAVerified()]
        return [permissions.IsAuthenticated()]
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
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsDoubleFAVerified()]
        return [permissions.IsAuthenticated()]
    class BookStatsSerializer(serializers.Serializer):
        total_books = serializers.IntegerField()
        avg_publication_year = serializers.FloatField()
        oldest_book_year = serializers.IntegerField()
        newest_book_year = serializers.IntegerField()
        most_popular_author = serializers.CharField()
        books_by_popular_author = serializers.IntegerField()
  
    @action(detail=False, methods=['GET'], url_path='export-excel')
    def export_books_to_excel(self, request, *args, **kwargs):
        books = Book.objects.all()
       
        wb = Workbook()
        ws = wb.active
        ws.title = "Книги библиотеки"
        
        headers = ['Название', 'Автор', 'Жанр', 'Год издания', 'Описание']
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal='center')
        
        for row, book in enumerate(books, 2):
            ws.cell(row=row, column=1, value=book.name)
            ws.cell(row=row, column=2, value=book.author.nameAuthor)
            ws.cell(row=row, column=3, value=book.genres.name )
            ws.cell(row=row, column=4, value=book.publication_year)
            ws.cell(row=row, column=5, value=book.description)
        
        # размерность столбцов 
        for column in ws.columns: 
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            ws.column_dimensions[column_letter].width = adjusted_width
        
        buffer = io.BytesIO()
        wb.save(buffer)
        buffer.seek(0)
        
        response = HttpResponse(
            buffer.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="library_books.xlsx"'
        
        return response
     
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
  

class IsDoubleFAVerified(permissions.BasePermission):
    
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
            
        is_doublefaq = request.session.get('doublefaq_active', False)
        doublefaq_expires = request.session.get('doublefaq_expires')
        
        # Проверяем активна ли 2FA и не истекла ли
        if is_doublefaq and doublefaq_expires:
            if timezone.now().timestamp() > doublefaq_expires:
                request.session['doublefaq_active'] = False
                return False
            return True
        
        return False
      
class UserViewSet(viewsets.GenericViewSet):
    permission_classes = []

    @action(detail=False, url_path="info", methods=["GET"])
    def get_info(self, request, *args, **kwargs):
        # Проверяем 2FA статус из сессии
        is_doublefaq = request.session.get('doublefaq_active', False)
        doublefaq_expires = request.session.get('doublefaq_expires')
        
        # Проверяем не истекла ли сессия 2FA
        if is_doublefaq and doublefaq_expires:
            if timezone.now().timestamp() > doublefaq_expires:
                is_doublefaq = False
                request.session['doublefaq_active'] = False
        
        return Response({
            "username": request.user.username,
            "is_authenticated": request.user.is_authenticated,
            "is_staff": request.user.is_staff,
            "is_doublefaq": is_doublefaq,
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
    
    @action(detail=False, url_path="generate-2fa", methods=["POST"])
    def generate_2fa(self, request, *args, **kwargs):
        
        faq_code = str(random.randint(100000, 999999))
        
        
        request.session['faq_code'] = faq_code
        request.session['faq_code_expires'] = (timezone.now() + timedelta(minutes=5)).timestamp()
        
        
        print(f"2FA Code for {request.user.username}: {faq_code}")
        print(f"Код действителен до: {timezone.now() + timedelta(minutes=5)}")
        
        return Response({
            'success': True,
            'message': 'Код 2FA сгенерирован'
        })
    
    @action(detail=False, url_path="verify-2fa", methods=["POST"])
    def verify_2fa(self, request, *args, **kwargs):
     
        
        code = request.data.get('code', '')
        stored_code = request.session.get('faq_code')
        code_expires = request.session.get('faq_code_expires')
        
        # Проверяем существование и срок кода
     
        
        if timezone.now().timestamp() > code_expires:
            return Response({
                'success': False,
                'message': 'Код истек, запросите новый'
            })
        
        if code == stored_code:
            # Устанавливаем 2FA сессию на 1 минуту
            request.session['doublefaq_active'] = True
            request.session['doublefaq_expires'] = (timezone.now() + timedelta(minutes=1)).timestamp()
            
            # Очищаем использованный код
            del request.session['faq_code']
            del request.session['faq_code_expires']
            
            return Response({
                'success': True,
                'message': 'Двухфакторная аутентификация пройдена'
            })
        else:
            return Response({
                'success': False,
                'message': 'Неверный код'
            })
    
    @action(detail=False, url_path="logout", methods=["POST"])
    def logout_user(self, request, *args, **kwargs):
        # Очищаем все сессии
        request.session.flush()
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
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsDoubleFAVerified()]
        return [permissions.IsAuthenticated()]
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
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsDoubleFAVerified()]
        return [permissions.IsAuthenticated()]

    
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