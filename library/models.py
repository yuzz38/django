from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import post_delete


class Author(models.Model):
    nameAuthor = models.TextField("ФИО")
    bio = models.TextField("Биография")

    def __str__(self) -> str:
        return self.nameAuthor

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"


class Genre(models.Model):
    name = models.TextField("Название жанра")
    description = models.TextField("Описание жанра")

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Book(models.Model):
    name = models.TextField("Название")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Автор", null=True, blank=True)
    genres = models.ManyToManyField(Genre, verbose_name="Жанры")
    
    publication_year = models.IntegerField("Год публикации")
    description = models.TextField("Описание")
    
    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"


class Reader(models.Model):
    first_name = models.TextField("Имя")
    last_name = models.TextField("Фамилия")
    email = models.EmailField("Email")
    card_number = models.CharField("Номер читательского билета")
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE, null=True)
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Читатель"
        verbose_name_plural = "Читатели"


class BookInstance(models.Model):
    STATUS_CHOICES = [
        ('available', 'На полке'),
        ('borrowed', 'Выдана'),
        ('maintenance', 'В ремонте'),
    ]
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Книга")
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default='available')
    due_back = models.DateField("Дата возврата", null=True, blank=True)
    borrower = models.ForeignKey(Reader, on_delete=models.SET_NULL, verbose_name="Читатель", null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.book.name} - {self.get_status_display()}"

    class Meta:
        verbose_name = "Экземпляр книги"
        verbose_name_plural = "Экземпляры книг"


# Сигнал для автоматического создания пользователя при создании читателя
@receiver(post_save, sender=Reader)
def create_user_for_reader(sender, instance, created, **kwargs):
  
    if created:
        # Формируем username из имени и фамилии
        username_base = f"{instance.first_name}_{instance.last_name}"
        
        
        
        try:
            # Создаем пользователя без пароля
            user = User.objects.create_user(
                username=username_base,
                email=instance.email,
                password=None,  # Пароль не устанавливаем
                first_name=instance.first_name,
                last_name=instance.last_name
            )
            
            
        except Exception as e:
            print(f"Ошибка при создании пользователя: {e}")

# Сигнал для обновления пользователя при изменении читателя
@receiver(post_save, sender=Reader)
def update_user_for_reader(sender, instance, created, **kwargs):
   
    if not created:  
        try:
          
            user = User.objects.get(email=instance.email)
            
           
            user.first_name = instance.first_name
            user.last_name = instance.last_name
            
           
            new_username = f"{instance.first_name}_{instance.last_name}"
            if user.username != new_username:
               
                if not User.objects.filter(username=new_username).exclude(id=user.id).exists():
                    user.username = new_username
                else:
                    
                    counter = 1
                    while User.objects.filter(username=f"{new_username}_{counter}").exists():
                        counter += 1
                    user.username = f"{new_username}_{counter}"
            
            user.save()
            
       
        except Exception as e:
            print(f"Ошибка при обновлении пользователя: {e}")

# Сигнал для удаления читателя при удалении пользователя
@receiver(post_delete, sender=User)
def delete_reader_on_user_delete(sender, instance, **kwargs):

    try:
        
        if instance.email:
            reader = Reader.objects.filter(email=instance.email).first()
            if reader:
                reader.delete()
                print(f"Удален читатель {reader} при удалении пользователя {instance.username}")
                return
        
        
                
    except Exception as e:
        print(f"Ошибка при удалении читателя: {e}")