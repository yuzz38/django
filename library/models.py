from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import post_delete

class Author(models.Model):
    nameAuthor = models.TextField("ФИО")
    bio = models.TextField("Биография")
    picture = models.ImageField("Изображение", null=True, upload_to="library_img")
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
    genres = models.ForeignKey(Genre, on_delete=models.CASCADE, verbose_name="Жанры", null=True, blank=True)
    
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
    picture = models.ImageField("Фото", null=True, upload_to="library_img")
    totp_key = models.CharField(max_length=128, null=True)
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
        username = f"{instance.first_name}_{instance.last_name}"
        try:
            user = User.objects.create_user(
                username=username,
                email=instance.email,
                password=username, 
                first_name=instance.first_name,
                last_name=instance.last_name
            )
            instance.user = user
            import pyotp
            instance.totp_key = pyotp.random_base32()
            instance.save()
        except Exception as e:
            print(f"Ошибка при создании пользователя: {e}")

# Сигнал для обновления пользователя при изменении читателя
@receiver(post_save, sender=Reader)
def update_user_for_reader(sender, instance, created, **kwargs):
    if not created and instance.user:  
        try:
          
            instance.user.first_name = instance.first_name
            instance.user.last_name = instance.last_name
            instance.user.email = instance.email
            
            new_username = f"{instance.first_name}_{instance.last_name}"
            if instance.user.username != new_username:
                instance.user.username = new_username
            
        
            instance.user.save()
            
        except Exception as e:
            print(f"Ошибка при обновлении пользователя: {e}")

            
@receiver(post_delete, sender=Reader)
def delete_user_for_reader(sender, instance, **kwargs):
    try:
        if instance.email:
            user = User.objects.filter(email=instance.email).first()
            if user:
                user.delete()
            
    except Exception as e:
        print(f"Ошибка при удалении пользователя: {e}")