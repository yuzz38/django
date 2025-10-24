from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
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