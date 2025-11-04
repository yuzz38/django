import random
from django.core.management.base import BaseCommand

from faker import Faker

from library.models import Author, Genre, Book

from faker.providers import DynamicProvider
class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker(['ru_RU'])
       
        for _ in range(970):

            random_author = random.choice(Author.objects.all())
            random_genre = random.choice(Genre.objects.all())
            publication_year = random.randint(1900, 2024)
            Book.objects.create(
                name=fake.catch_phrase(), 
                author=random_author,
                genres=random_genre, 
                publication_year=publication_year,
                description=fake.text(max_nb_chars=300)
            )
        # for _ in range(990):
        #     Author.objects.create(
        #         nameAuthor=fake.name(),
        #         bio=fake.text(max_nb_chars=200)
        #     )  
    
    #     genres_data = DynamicProvider (
    #         provider_name="genres",
    #         elements=["Фантастика",
    # "Фэнтези", 
    # "Детектив",
    # "Роман",
    # "Триллер",
    # "Ужасы",
    # "Приключения",
    # "Исторический",
    # "Биография",
    # "Научпоп",
    # "Поэзия",
    # "Драма",
    # "Комедия",
    # "Классика",
    # "Психология",
    # "Философия",
    # "Бизнес",
    # "Кулинария",
    # "Справочная",
    # "Детская"],
    #     )
        
    #     fake.add_provider(genres_data)
    #     for _ in range(10):
    #         Genre.objects.create(
    #             name=fake.genres(),
    #             description=fake.text(max_nb_chars=200)
    #         )  
