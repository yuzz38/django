from django.core.management.base import BaseCommand

from faker import Faker

from library.models import Author, Genre, Book

from faker.providers import DynamicProvider
class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker(['ru_RU'])
        
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
    #     for _ in range(990):
    #         Genre.objects.create(
    #             name=fake.genres(),
    #             description=fake.text(max_nb_chars=200)
    #         )  