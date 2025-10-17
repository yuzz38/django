from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from library.models import Author, Book, Genre, Reader, BookInstance


class AuthorCRUDTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.author_data = {
            'nameAuthor': 'Лев Толстой',
            'bio': 'Русский писатель, философ'
        }
        self.author = Author.objects.create(**self.author_data)
        self.list_url = reverse('authors-list')
        self.detail_url = reverse('authors-detail', kwargs={'pk': self.author.pk})

    def test_create_author(self):
        """Тест создания автора"""
        new_author_data = {
            'nameAuthor': 'Фёдор Достоевский',
            'bio': 'Русский писатель, мыслитель'
        }
        response = self.client.post(self.list_url, new_author_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 2)
        self.assertEqual(Author.objects.get(id=response.data['id']).nameAuthor, 'Фёдор Достоевский')


    def test_read_author_detail(self):
        """Тест чтения конкретного автора"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nameAuthor'], self.author_data['nameAuthor'])
        self.assertEqual(response.data['bio'], self.author_data['bio'])

    def test_update_author(self):
        """Тест обновления автора"""
        updated_data = {
            'nameAuthor': 'Лев Толстой (обновленный)',
            'bio': 'Обновленная биография'
        }
        response = self.client.put(self.detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.author.refresh_from_db()
        self.assertEqual(self.author.nameAuthor, 'Лев Толстой (обновленный)')

    def test_delete_author(self):
        """Тест удаления автора"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Author.objects.count(), 0)

class GenreCRUDTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.genre_data = {
            'name': 'Роман',
            'description': 'Большое повествовательное произведение'
        }
        self.genre = Genre.objects.create(**self.genre_data)
        self.list_url = reverse('genres-list')
        self.detail_url = reverse('genres-detail', kwargs={'pk': self.genre.pk})

    def test_create_genre(self):
        """Тест создания жанра"""
        new_genre_data = {
            'name': 'Фантастика',
            'description': 'Произведения о вымышленных мирах'
        }
        response = self.client.post(self.list_url, new_genre_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Genre.objects.count(), 2)


    def test_read_genre_detail(self):
        """Тест чтения конкретного жанра"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.genre_data['name'])

    def test_update_genre(self):
        """Тест обновления жанра"""
        updated_data = {
            'name': 'Роман (обновленный)',
            'description': 'Обновленное описание'
        }
        response = self.client.put(self.detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.genre.refresh_from_db()
        self.assertEqual(self.genre.name, 'Роман (обновленный)')

    def test_delete_genre(self):
        """Тест удаления жанра"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Genre.objects.count(), 0)

class BookCRUDTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Создаем необходимые объекты
        self.author = Author.objects.create(
            nameAuthor='Александр Пушкин',
            bio='Русский поэт'
        )
        self.genre1 = Genre.objects.create(name='Поэзия', description='Стихотворные произведения')
        self.genre2 = Genre.objects.create(name='Классика', description='Классическая литература')
        
        self.book_data = {
            'name': 'Евгений Онегин',
            'author': self.author.id,
            'publication_year': 1833,
            'description': 'Роман в стихах',
            'genres': [self.genre1.id, self.genre2.id]
        }
        
        self.book = Book.objects.create(
            name=self.book_data['name'],
            author=self.author,
            publication_year=self.book_data['publication_year'],
            description=self.book_data['description']
        )
        self.book.genres.set([self.genre1.id, self.genre2.id])
        
        self.list_url = reverse('books-list')
        self.detail_url = reverse('books-detail', kwargs={'pk': self.book.pk})

    def test_create_book(self):
        """Тест создания книги"""
        new_book_data = {
            'name': 'Капитанская дочка',
            'author': self.author.id,
            'publication_year': 1836,
            'description': 'Исторический роман',
            'genres': [self.genre1.id]
        }
        response = self.client.post(self.list_url, new_book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)


    def test_read_book_detail(self):
        """Тест чтения конкретной книги"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.book_data['name'])

    def test_update_book(self):
        """Тест обновления книги"""
        updated_data = {
            'name': 'Евгений Онегин (обновленный)',
            'author': self.author.id,
            'publication_year': 1833,
            'description': 'Обновленное описание',
            'genres': [self.genre1.id]
        }
        response = self.client.put(self.detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.name, 'Евгений Онегин (обновленный)')

    def test_delete_book(self):
        """Тест удаления книги"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

class ReaderCRUDTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.reader_data = {
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'email': 'ivan@example.com',
            'card_number': '12345'
        }
        self.reader = Reader.objects.create(**self.reader_data)
        self.list_url = reverse('readers-list')
        self.detail_url = reverse('readers-detail', kwargs={'pk': self.reader.pk})

    def test_create_reader(self):
        """Тест создания читателя"""
        new_reader_data = {
            'first_name': 'Петр',
            'last_name': 'Петров',
            'email': 'petr@example.com',
            'card_number': '54321'
        }
        response = self.client.post(self.list_url, new_reader_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reader.objects.count(), 2)


    def test_read_reader_detail(self):
        """Тест чтения конкретного читателя"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], self.reader_data['first_name'])

    def test_update_reader(self):
        """Тест обновления читателя"""
        updated_data = {
            'first_name': 'Иван (обновленный)',
            'last_name': 'Иванов',
            'email': 'ivan.new@example.com',
            'card_number': '12345'
        }
        response = self.client.put(self.detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.reader.refresh_from_db()
        self.assertEqual(self.reader.first_name, 'Иван (обновленный)')

    def test_delete_reader(self):
        """Тест удаления читателя"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Reader.objects.count(), 0)

class BookInstanceCRUDTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        
        self.author = Author.objects.create(
            nameAuthor='Михаил Лермонтов',
            bio='Русский поэт'
        )
        self.genre = Genre.objects.create(name='Поэзия', description='Стихотворные произведения')
        self.book = Book.objects.create(
            name='Герой нашего времени',
            author=self.author,
            publication_year=1840,
            description='Психологический роман'
        )
        self.book.genres.add(self.genre)
        
        self.reader = Reader.objects.create(
            first_name='Сергей',
            last_name='Сергеев',
            email='sergey@example.com',
            card_number='67890'
        )
        
        self.book_instance_data = {
            'book': self.book.id,
            'status': 'available',
            'due_back': None,
            'borrower': None
        }
        
        self.book_instance = BookInstance.objects.create(
            book=self.book,
            status='available'
        )
        
        self.list_url = reverse('bookinstances-list')
        self.detail_url = reverse('bookinstances-detail', kwargs={'pk': self.book_instance.pk})

    def test_create_book_instance(self):
        """Тест создания экземпляра книги"""
        new_instance_data = {
            'book': self.book.id,
            'status': 'borrowed',
            'due_back': '2024-12-31',
            'borrower': self.reader.id
        }
        response = self.client.post(self.list_url, new_instance_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BookInstance.objects.count(), 2)


    def test_read_book_instance_detail(self):
        """Тест чтения конкретного экземпляра книги"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'available')

    def test_update_book_instance(self):
        """Тест обновления экземпляра книги"""
        updated_data = {
            'book': self.book.id,
            'status': 'borrowed',
            'due_back': '2024-12-31',
            'borrower': self.reader.id
        }
        response = self.client.put(self.detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book_instance.refresh_from_db()
        self.assertEqual(self.book_instance.status, 'borrowed')

    def test_delete_book_instance(self):
        """Тест удаления экземпляра книги"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(BookInstance.objects.count(), 0)
