import pytest
from django.urls import reverse
from rest_framework import status

from users.models import *
from main.models import *


@pytest.mark.django_db
class TestAuthorViewSet:
    @pytest.fixture(autouse=True)
    def setup(self, setup_users):
        self.client = setup_users["client"]

        self.regular_user_token = setup_users["regular_user_token"]
        self.bookspace_owner_token = setup_users["bookspace_owner_token"]
        self.bookspace_manager_token = setup_users["bookspace_manager_token"]
        self.asst_bookspace_manager_token = setup_users["asst_bookspace_manager_token"]
        self.bookspace_worker_token = setup_users["bookspace_worker_token"]

    def test_create_author_as_bookspace_owner(self):
        """
        Test creating a author by a bookspace owner.
        """
        author_data = {'first_name': 'David', 'last_name': 'Karanja'}
        response = self.client.post(reverse('main:authors-list'), data=author_data,
                                    HTTP_AUTHORIZATION=f'Token {self.bookspace_owner_token}')
        assert response.status_code == status.HTTP_201_CREATED
        assert Author.objects.filter(first_name=author_data['first_name']).exists()

    def test_create_author_as_bookspace_manager(self):
        """
        Test creating a author by a bookspace manager
        """
        author_data = {'first_name': 'Henriette', 'last_name': 'Uwiyezimana'}
        response = self.client.post(
            reverse('main:authors-list'), author_data, HTTP_AUTHORIZATION=f'Token {self.bookspace_manager_token}')
        assert response.status_code == status.HTTP_201_CREATED
        assert Author.objects.filter(first_name=author_data['first_name']).exists()

    def test_create_author_as_asst_bookspace_manager(self):
        """
        Test creating a author by a assistant bookspace manager (should be denied).
        """
        author_data = {'first_name': 'Henriette', 'last_name': 'Uwiyezimana'}
        response = self.client.post(
            reverse('main:authors-list'), author_data,
            HTTP_AUTHORIZATION=f'Token {self.asst_bookspace_manager_token}')
        assert response.status_code == status.HTTP_201_CREATED
        assert Author.objects.filter(first_name=author_data['first_name']).exists()

    def test_create_author_as_bookspace_worker_permission_denied(self):
        """
        Test creating a author by a bookspace worker (should be denied).
        """
        author_data = {'first_name': 'Peter', 'last_name': 'Evance'}
        response = self.client.post(reverse('main:authors-list'), author_data,
                                    HTTP_AUTHORIZATION=f'Token {self.bookspace_worker_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not Author.objects.filter(first_name=author_data['first_name']).exists()

    def test_create_author_as_regular_user_permission_denied(self):
        """
        Test creating a author by a regular user (should be denied).
        """
        author_data = {'first_name': 'Henriette', 'last_name': 'Uwiyezimana'}
        response = self.client.post(reverse('main:authors-list'), author_data,
                                    HTTP_AUTHORIZATION=f'Token {self.regular_user_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not Author.objects.filter(first_name=author_data['first_name']).exists()

    def test_create_author_without_authentication(self):
        """
        Test creating a author without authentication (should be denied).
        """
        author_data = {'first_name': 'Henriette', 'last_name': 'Uwiyezimana'}
        response = self.client.post(reverse('main:authors-list'), author_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert not Author.objects.filter(first_name=author_data['first_name']).exists()

    def test_retrieve_authors_as_bookspace_owner(self):
        """
        Test retrieving authors by a bookspace owner.
        """
        response = self.client.get(reverse('main:authors-list'),
                                   HTTP_AUTHORIZATION=f'Token {self.bookspace_owner_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_authors_as_bookspace_manager(self):
        """
        Test retrieving authors by a bookspace manager.
        """
        response = self.client.get(reverse('main:authors-list'),
                                   HTTP_AUTHORIZATION=f'Token {self.bookspace_manager_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_authors_as_asst_bookspace_manager(self):
        """
        Test retrieving authors by an assistant bookspace manager.
        """
        response = self.client.get(reverse('main:authors-list'),
                                   HTTP_AUTHORIZATION=f'Token {self.asst_bookspace_manager_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_authors_as_regular_user_permission_denied(self):
        """
        Test retrieving authors by a regular user (should be denied).
        """
        response = self.client.get(reverse('main:authors-list'),
                                   HTTP_AUTHORIZATION=f'Token {self.regular_user_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_authors_without_authentication(self):
        """
        Test retrieving authors without authentication (should be denied).
        """
        url = reverse('main:authors-list')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_author_as_bookspace_owner(self):
        """
        Test updating an author as bookspace owner
        """
        author = Author.objects.create(first_name='Test', last_name='One')
        url = reverse('main:authors-detail', kwargs={'pk': author.id})
        author_update_data = {'first_name': 'first'}
        response = self.client.patch(url, author_update_data, HTTP_AUTHORIZATION=f'Token {self.bookspace_owner_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_update_author_as_bookspace_manager(self):
        """
        Test updating an author as bookspace manager
        """
        author = Author.objects.create(first_name='Test', last_name='One')
        url = reverse('main:authors-detail', kwargs={'pk': author.id})
        author_update_data = {'first_name': 'first'}
        response = self.client.patch(url, author_update_data,
                                     HTTP_AUTHORIZATION=f'Token {self.bookspace_manager_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_update_author_as_asst_bookspace_manager(self):
        """
        Test updating an author as assistant bookspace manager
        """
        author = Author.objects.create(first_name='Test', last_name='One')
        url = reverse('main:authors-detail', kwargs={'pk': author.id})
        author_update_data = {'first_name': 'first'}
        response = self.client.patch(url, author_update_data,
                                     HTTP_AUTHORIZATION=f'Token {self.asst_bookspace_manager_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_update_author_as_bookspace_worker_permission_denied(self):
        """
        Test updating an author as bookspace worker (permission denied)
        """
        author = Author.objects.create(first_name='Test', last_name='One')
        url = reverse('main:authors-detail', kwargs={'pk': author.id})
        author_update_data = {'first_name': 'first'}
        response = self.client.patch(url, author_update_data, HTTP_AUTHORIZATION=f'Token {self.bookspace_worker_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_author_as_regular_user_permission_denied(self):
        """
        Test updating an author as regular (permission denied)
        """
        author = Author.objects.create(first_name='Test', last_name='One')
        url = reverse('main:authors-detail', kwargs={'pk': author.id})
        author_update_data = {'first_name': 'first'}
        response = self.client.patch(url, author_update_data, HTTP_AUTHORIZATION=f'Token {self.regular_user_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_author_without_authentication(self):
        """
        Test updating an author without authentication
        """
        author = Author.objects.create(first_name='Test', last_name='One')
        url = reverse('main:authors-detail', kwargs={'pk': author.id})
        author_update_data = {'first_name': 'first'}
        response = self.client.patch(url, author_update_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_author_as_bookspace_owner(self):
        """
        Test deleting a author by a bookspace owner.
        """
        author = Author.objects.create(first_name='Test', last_name='One')
        url = reverse('main:authors-detail', kwargs={'pk': author.id})
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Token {self.bookspace_owner_token}')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Author.objects.filter(id=author.id).exists()

    def test_delete_author_as_bookspace_manager(self):
        """
        Test deleting a author by a bookspace manager.
        """
        author = Author.objects.create(first_name='Test', last_name='One')
        url = reverse('main:authors-detail', kwargs={'pk': author.id})
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Token {self.bookspace_manager_token}')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Author.objects.filter(id=author.id).exists()

    def test_delete_author_as_asst_bookspace_manager(self):
        """
        Test deleting a author by an assistant bookspace manager.
        """
        author = Author.objects.create(first_name='Test', last_name='One')
        url = reverse('main:authors-detail', kwargs={'pk': author.id})
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Token {self.asst_bookspace_manager_token}')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Author.objects.filter(id=author.id).exists()

    def test_delete_author_as_bookspace_worker_permission_denied(self):
        """
        Test deleting a author by a bookspace worker (should be denied).
        """
        author = Author.objects.create(first_name='Test', last_name='One')
        url = reverse('main:authors-detail', kwargs={'pk': author.id})
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Token {self.bookspace_worker_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Author.objects.filter(id=author.id).exists()

    def test_delete_author_as_regular_user_permission_denied(self):
        '''
        Test delete author as a regular user (permission denied)
        '''
        author = Author.objects.create(first_name='Test', last_name='One')
        url = reverse('main:authors-detail', kwargs={'pk': author.id})

        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Token {self.regular_user_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Author.objects.filter(id=author.id).exists()

    def test_delete_author_unauthorized(self):
        '''
        Test delete author by unauthorized request
        '''
        author = Author.objects.create(first_name='Test', last_name='One')
        url = reverse('main:authors-detail', kwargs={'pk': author.id})

        response = self.client.delete(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert Author.objects.filter(id=author.id).exists()

    def test_filter_authors_by_name(self):
        """
        Test filtering authors by name (e.g., get all authors with name 'Stephen').
        """
        Author.objects.create(first_name='Stephen', last_name='Omondi')
        Author.objects.create(first_name='Test', last_name='One')
        url = reverse('main:authors-list')
        url += f'?first_name=Stephen'

        response = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.bookspace_owner_token}')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['first_name'] == 'Stephen'

    def test_filter_authors_by_partial_name(self):
        """
        Test filtering authors by name (e.g., get all authors with name 'Ste').
        """
        Author.objects.create(first_name='Stephen', last_name='Omondi')
        Author.objects.create(first_name='Test', last_name='One')
        url = reverse('main:authors-list')
        url += f'?first_name=Ste'

        response = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.bookspace_owner_token}')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['first_name'] == 'Stephen'

    def test_order_authors_by_multiple_fields(self):
        """
        Test ordering authors by multiple fields (e.g., first names in descending order, id in ascending order).
        """
        Author.objects.create(first_name='Stephen', last_name='Omondi')
        Author.objects.create(first_name='Peter', last_name='Evance')
        Author.objects.create(first_name='Henriette', last_name='Uwiyezimana')
        Author.objects.create(first_name='Test', last_name='One')
        url = reverse('main:authors-list')
        url += '?ordering=first_name'

        response = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.bookspace_manager_token}')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 4
        assert response.data[0]['first_name'] == 'Henriette'
        assert response.data[1]['first_name'] == 'Peter'
        assert response.data[2]['first_name'] == 'Stephen'
        assert response.data[3]['first_name'] == 'Test'

    def test_no_results_for_invalid_name(self):
        """
        Test filtering with a name that doesn't exist.
        """
        url = reverse('main:authors-list')
        url += '?name=nonexistent'
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.bookspace_manager_token}')
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data == {'detail': 'No author(s) found matching the provided filters.'}


@pytest.mark.django_db
class TestBookTagViewSet:
    @pytest.fixture(autouse=True)
    def setup(self, setup_users):
        self.client = setup_users["client"]

        self.regular_user_token = setup_users["regular_user_token"]
        self.bookspace_owner_token = setup_users["bookspace_owner_token"]
        self.bookspace_manager_token = setup_users["bookspace_manager_token"]
        self.asst_bookspace_manager_token = setup_users["asst_bookspace_manager_token"]
        self.bookspace_worker_token = setup_users["bookspace_worker_token"]

    def test_create_book_tag_as_bookspace_owner(self):
        """
        Test creating a book tag by a bookspace owner.
        """
        book_tag_data = {'name': BookTagChoices.HISTORY}
        response = self.client.post(reverse('main:book-tags-list'), data=book_tag_data,
                                    HTTP_AUTHORIZATION=f'Token {self.bookspace_owner_token}')
        assert response.status_code == status.HTTP_201_CREATED
        assert BookTag.objects.filter(name=book_tag_data['name']).exists()

    def test_create_book_tag_as_bookspace_manager(self):
        """
        Test creating a book tag by a bookspace manager
        """
        book_tag_data = {'name': BookTagChoices.HISTORY}
        response = self.client.post(
            reverse('main:book-tags-list'), book_tag_data, HTTP_AUTHORIZATION=f'Token {self.bookspace_manager_token}')
        assert response.status_code == status.HTTP_201_CREATED
        assert BookTag.objects.filter(name=book_tag_data['name']).exists()

    def test_create_book_tag_as_asst_bookspace_manager(self):
        """
        Test creating a book tag by a assistant bookspace manager (should be denied).
        """
        book_tag_data = {'name': BookTagChoices.HISTORY}
        response = self.client.post(
            reverse('main:book-tags-list'), book_tag_data,
            HTTP_AUTHORIZATION=f'Token {self.asst_bookspace_manager_token}')
        assert response.status_code == status.HTTP_201_CREATED
        assert BookTag.objects.filter(name=book_tag_data['name']).exists()

    def test_create_book_tag_as_bookspace_worker_permission_denied(self):
        """
        Test creating a book tag by a bookspace worker (should be denied).
        """
        book_tag_data = {'name': BookTagChoices.HISTORY}
        response = self.client.post(reverse('main:book-tags-list'), book_tag_data,
                                    HTTP_AUTHORIZATION=f'Token {self.bookspace_worker_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not BookTag.objects.filter(name=book_tag_data['name']).exists()

    def test_create_book_tag_as_regular_user_permission_denied(self):
        """
        Test creating a book tag by a regular user (should be denied).
        """
        book_tag_data = {'name': BookTagChoices.HISTORY}
        response = self.client.post(reverse('main:book-tags-list'), book_tag_data,
                                    HTTP_AUTHORIZATION=f'Token {self.regular_user_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not BookTag.objects.filter(name=book_tag_data['name']).exists()

    def test_create_book_tag_without_authentication(self):
        """
        Test creating a book tag without authentication (should be denied).
        """
        book_tag_data = {'name': BookTagChoices.HISTORY}
        response = self.client.post(reverse('main:book-tags-list'), book_tag_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert not BookTag.objects.filter(name=book_tag_data['name']).exists()

    def test_retrieve_book_tag_as_bookspace_owner(self):
        """
        Test retrieving book-tags by a bookspace owner.
        """
        response = self.client.get(reverse('main:book-tags-list'),
                                   HTTP_AUTHORIZATION=f'Token {self.bookspace_owner_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_book_tag_as_bookspace_manager(self):
        """
        Test retrieving book-tags by a bookspace manager.
        """
        response = self.client.get(reverse('main:book-tags-list'),
                                   HTTP_AUTHORIZATION=f'Token {self.bookspace_manager_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_book_tags_as_asst_bookspace_manager(self):
        """
        Test retrieving book-tags by an assistant bookspace manager.
        """
        response = self.client.get(reverse('main:book-tags-list'),
                                   HTTP_AUTHORIZATION=f'Token {self.asst_bookspace_manager_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_book_tags_as_regular_user_permission_denied(self):
        """
        Test retrieving book-tags by a regular user (should be denied).
        """
        response = self.client.get(reverse('main:book-tags-list'),
                                   HTTP_AUTHORIZATION=f'Token {self.regular_user_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_book_tags_without_authentication(self):
        """
        Test retrieving book-tags without authentication (should be denied).
        """
        url = reverse('main:book-tags-list')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_book_tags_as_bookspace_owner(self):
        """
        Test updating a book_tag as bookspace owner
        """
        book_tag = BookTag.objects.create(name={BookTagChoices.FICTION})
        url = reverse('main:book-tags-detail', kwargs={'pk': book_tag.id})
        book_tag_update_data = {'name': {BookTagChoices.ADVENTURE}}
        response = self.client.patch(url, book_tag_update_data,
                                     HTTP_AUTHORIZATION=f'Token {self.bookspace_owner_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_update_book_tags_as_bookspace_manager(self):
        """
        Test updating a book_tag as bookspace manager
        """
        book_tag = BookTag.objects.create(name={BookTagChoices.FICTION})
        url = reverse('main:book-tags-detail', kwargs={'pk': book_tag.id})
        book_tag_update_data = {'name': {BookTagChoices.ADVENTURE}}
        response = self.client.patch(url, book_tag_update_data,
                                     HTTP_AUTHORIZATION=f'Token {self.bookspace_manager_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_update_book_tags_as_asst_bookspace_manager(self):
        """
        Test updating a book_tag as assistant bookspace manager
        """
        book_tag = BookTag.objects.create(name={BookTagChoices.FICTION})
        url = reverse('main:book-tags-detail', kwargs={'pk': book_tag.id})
        book_tag_update_data = {'name': {BookTagChoices.ADVENTURE}}
        response = self.client.patch(url, book_tag_update_data,
                                     HTTP_AUTHORIZATION=f'Token {self.asst_bookspace_manager_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_update_book_tags_as_bookspace_worker_permission_denied(self):
        """
        Test updating a book_tag as bookspace worker (permission denied)
        """
        book_tag = BookTag.objects.create(name={BookTagChoices.FICTION})
        url = reverse('main:book-tags-detail', kwargs={'pk': book_tag.id})
        book_tag_update_data = {'name': {BookTagChoices.ADVENTURE}}
        response = self.client.patch(url, book_tag_update_data,
                                     HTTP_AUTHORIZATION=f'Token {self.bookspace_worker_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_book_tags_as_regular_user_permission_denied(self):
        """
        Test updating a book_tag as regular (permission denied)
        """
        book_tag = BookTag.objects.create(name={BookTagChoices.FICTION})
        url = reverse('main:book-tags-detail', kwargs={'pk': book_tag.id})
        book_tag_update_data = {'name': {BookTagChoices.ADVENTURE}}
        response = self.client.patch(url, book_tag_update_data, HTTP_AUTHORIZATION=f'Token {self.regular_user_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_book_tags_without_authentication(self):
        """
        Test updating a book_tag without authentication
        """
        book_tag = BookTag.objects.create(name={BookTagChoices.FICTION})
        url = reverse('main:book-tags-detail', kwargs={'pk': book_tag.id})
        book_tag_update_data = {'name': {BookTagChoices.ADVENTURE}}
        response = self.client.patch(url, book_tag_update_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_book_tags_as_bookspace_owner(self):
        """
        Test deleting a author by a bookspace owner.
        """
        book_tag = BookTag.objects.create(name={BookTagChoices.FICTION})
        url = reverse('main:book-tags-detail', kwargs={'pk': book_tag.id})
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Token {self.bookspace_owner_token}')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not BookTag.objects.filter(id=book_tag.id).exists()

    def test_delete_book_tags_as_bookspace_manager(self):
        """
        Test deleting a author by a bookspace manager.
        """
        book_tag = BookTag.objects.create(name={BookTagChoices.FICTION})
        url = reverse('main:book-tags-detail', kwargs={'pk': book_tag.id})
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Token {self.bookspace_manager_token}')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not BookTag.objects.filter(id=book_tag.id).exists()

    def test_delete_book_tags_as_asst_bookspace_manager(self):
        """
        Test deleting a author by an assistant bookspace manager.
        """
        book_tag = BookTag.objects.create(name={BookTagChoices.FICTION})
        url = reverse('main:book-tags-detail', kwargs={'pk': book_tag.id})
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Token {self.asst_bookspace_manager_token}')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not BookTag.objects.filter(id=book_tag.id).exists()

    def test_delete_book_tags_as_bookspace_worker_permission_denied(self):
        """
        Test deleting a author by a bookspace worker (should be denied).
        """
        book_tag = BookTag.objects.create(name={BookTagChoices.FICTION})
        url = reverse('main:book-tags-detail', kwargs={'pk': book_tag.id})
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Token {self.bookspace_worker_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert BookTag.objects.filter(id=book_tag.id).exists()

    def test_delete_book_tags_as_regular_user_permission_denied(self):
        '''
        Test delete author as a regular user (permission denied)
        '''
        book_tag = BookTag.objects.create(name={BookTagChoices.FICTION})
        url = reverse('main:book-tags-detail', kwargs={'pk': book_tag.id})

        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Token {self.regular_user_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert BookTag.objects.filter(id=book_tag.id).exists()

    def test_delete_book_tags_unauthorized(self):
        '''
        Test delete author by unauthorized request
        '''
        book_tag = BookTag.objects.create(name={BookTagChoices.FICTION})
        url = reverse('main:book-tags-detail', kwargs={'pk': book_tag.id})

        response = self.client.delete(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert BookTag.objects.filter(id=book_tag.id).exists()

    def test_filter_book_tags_by_name(self):
        """
        Test filtering book-tags by name (e.g., get all book-tags with name 'Fiction').
        """
        BookTag.objects.create(name=BookTagChoices.FICTION)
        BookTag.objects.create(name=BookTagChoices.ROMANCE)
        url = reverse('main:book-tags-list')
        url += f'?name=Fiction'

        response = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.bookspace_owner_token}')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['name'] == 'Fiction'

    def test_filter_book_tags_by_partial_name(self):
        """
        Test filtering book-tags by name (e.g., get all book-tags with name 'Fi').
        """

        BookTag.objects.create(name=BookTagChoices.FICTION)
        BookTag.objects.create(name=BookTagChoices.ROMANCE)
        url = reverse('main:book-tags-list')
        url += f'?name=Fi'

        response = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.bookspace_owner_token}')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['name'] == 'Fiction'

    def test_order_book_tags_by_multiple_fields(self):
        """
        Test ordering book-tags by multiple fields (e.g., first names in descending order, id in ascending order).
        """
        BookTag.objects.create(name=BookTagChoices.FICTION)
        BookTag.objects.create(name=BookTagChoices.ROMANCE)
        url = reverse('main:book-tags-list')
        url += '?ordering=name'

        response = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.bookspace_manager_token}')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        print(response.data[0]['name'])
        # assert response.data[0]['name'] == 'Fiction'
        # assert response.data[1]['name'] == 'Romance'

    def test_no_results_for_invalid__book_tag_name(self):
        """
        Test filtering with a name that doesn't exist.
        """
        url = reverse('main:book-tags-list')
        url += '?name=nonexistent'
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.bookspace_manager_token}')
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data == {'detail': 'No book tag(s) found matching the provided filters.'}


@pytest.mark.django_db
class TestBookViewSet:
    @pytest.fixture(autouse=True)
    def setup(self, setup_users, setup_book_data):
        self.client = setup_users["client"]

        self.regular_user_token = setup_users["regular_user_token"]
        self.bookspace_owner_token = setup_users["bookspace_owner_token"]
        self.bookspace_manager_token = setup_users["bookspace_manager_token"]
        self.asst_bookspace_manager_token = setup_users["asst_bookspace_manager_token"]
        self.bookspace_worker_token = setup_users["bookspace_worker_token"]

        self.book_data = setup_book_data["book_data"]

    def test_create_book_as_bookspace_owner(self):
        """
        Test creating a book by a bookspace owner.
        """
        response = self.client.post(reverse('main:books-list'), data=self.book_data,
                                    HTTP_AUTHORIZATION=f'Token {self.bookspace_owner_token}')
        assert response.status_code == status.HTTP_201_CREATED
        assert Book.objects.filter(name=self.book_data['name']).exists()

    def test_create_book_as_bookspace_manager(self):
        """
        Test creating a book by a bookspace manager
        """

        response = self.client.post(
            reverse('main:books-list'), self.book_data, HTTP_AUTHORIZATION=f'Token {self.bookspace_manager_token}')
        assert response.status_code == status.HTTP_201_CREATED
        assert Book.objects.filter(name=self.book_data['name']).exists()

    def test_create_book_as_asst_bookspace_manager(self):
        """
        Test creating a book by a assistant bookspace manager.
        """

        response = self.client.post(
            reverse('main:books-list'), self.book_data,
            HTTP_AUTHORIZATION=f'Token {self.asst_bookspace_manager_token}')
        assert response.status_code == status.HTTP_201_CREATED
        assert Book.objects.filter(name=self.book_data['name']).exists()

    def test_create_book_as_bookspace_worker(self):
        """
        Test creating a book by a bookspace worker.
        """

        response = self.client.post(reverse('main:books-list'), self.book_data,
                                    HTTP_AUTHORIZATION=f'Token {self.bookspace_worker_token}')
        assert response.status_code == status.HTTP_201_CREATED
        assert Book.objects.filter(name=self.book_data['name']).exists()

    def test_create_book_as_regular_user_permission_denied(self):
        """
        Test creating a book by a regular user (should be denied).
        """

        response = self.client.post(reverse('main:books-list'), self.book_data,
                                    HTTP_AUTHORIZATION=f'Token {self.regular_user_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not Book.objects.filter(name=self.book_data['name']).exists()

    def test_create_book_without_authentication(self):
        """
        Test creating a book without authentication (should be denied).
        """

        response = self.client.post(reverse('main:books-list'), self.book_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert not Book.objects.filter(name=self.book_data['name']).exists()

    def test_retrieve_book_as_bookspace_owner(self):
        """
        Test retrieving book-tags by a bookspace owner.
        """
        response = self.client.get(reverse('main:books-list'),
                                   HTTP_AUTHORIZATION=f'Token {self.bookspace_owner_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_book_as_bookspace_manager(self):
        """
        Test retrieving book-tags by a bookspace manager.
        """
        response = self.client.get(reverse('main:books-list'),
                                   HTTP_AUTHORIZATION=f'Token {self.bookspace_manager_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_books_as_asst_bookspace_manager(self):
        """
        Test retrieving book-tags by an assistant bookspace manager.
        """
        response = self.client.get(reverse('main:books-list'),
                                   HTTP_AUTHORIZATION=f'Token {self.asst_bookspace_manager_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_books_as_regular_user(self):
        """
        Test retrieving book-tags by a regular user.
        """
        response = self.client.get(reverse('main:books-list'),
                                   HTTP_AUTHORIZATION=f'Token {self.regular_user_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_books_without_authentication(self):
        """
        Test retrieving book-tags without authentication.
        """
        url = reverse('main:books-list')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_update_books_as_bookspace_owner(self):
        """
        Test updating a book_tag as bookspace owner
        """
        book = Book.objects.create(**self.book_data)
        url = reverse('main:books-detail', kwargs={'pk': book.id})
        book_update_data = {'name': "Test Book Title"}
        response = self.client.patch(url, book_update_data,
                                     HTTP_AUTHORIZATION=f'Token {self.bookspace_owner_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_update_books_as_bookspace_manager(self):
        """
        Test updating a book_tag as bookspace manager
        """
        book_tag = BookTag.objects.create(name={BookTagChoices.FICTION})
        url = reverse('main:books-detail', kwargs={'pk': book_tag.id})
        book_tag_update_data = {'name': {BookTagChoices.ADVENTURE}}
        response = self.client.patch(url, book_tag_update_data,
                                     HTTP_AUTHORIZATION=f'Token {self.bookspace_manager_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_update_books_as_asst_bookspace_manager(self):
        """
        Test updating a book_tag as assistant bookspace manager
        """
        book_tag = BookTag.objects.create(name={BookTagChoices.FICTION})
        url = reverse('main:books-detail', kwargs={'pk': book_tag.id})
        book_tag_update_data = {'name': {BookTagChoices.ADVENTURE}}
        response = self.client.patch(url, book_tag_update_data,
                                     HTTP_AUTHORIZATION=f'Token {self.asst_bookspace_manager_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_update_books_as_bookspace_worker_permission_denied(self):
        """
        Test updating a book_tag as bookspace worker (permission denied)
        """
        book_tag = BookTag.objects.create(name={BookTagChoices.FICTION})
        url = reverse('main:books-detail', kwargs={'pk': book_tag.id})
        book_tag_update_data = {'name': {BookTagChoices.ADVENTURE}}
        response = self.client.patch(url, book_tag_update_data,
                                     HTTP_AUTHORIZATION=f'Token {self.bookspace_worker_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_books_as_regular_user_permission_denied(self):
        """
        Test updating a book_tag as regular (permission denied)
        """
        book_tag = BookTag.objects.create(name={BookTagChoices.FICTION})
        url = reverse('main:books-detail', kwargs={'pk': book_tag.id})
        book_tag_update_data = {'name': {BookTagChoices.ADVENTURE}}
        response = self.client.patch(url, book_tag_update_data, HTTP_AUTHORIZATION=f'Token {self.regular_user_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_books_without_authentication(self):
        """
        Test updating a book_tag without authentication
        """
        book_tag = BookTag.objects.create(name={BookTagChoices.FICTION})
        url = reverse('main:books-detail', kwargs={'pk': book_tag.id})
        book_tag_update_data = {'name': {BookTagChoices.ADVENTURE}}
        response = self.client.patch(url, book_tag_update_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_books_as_bookspace_owner(self):
        """
        Test deleting a author by a bookspace owner.
        """
        book_tag = BookTag.objects.create(name={BookTagChoices.FICTION})
        url = reverse('main:books-detail', kwargs={'pk': book_tag.id})
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Token {self.bookspace_owner_token}')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not BookTag.objects.filter(id=book_tag.id).exists()

    def test_delete_books_as_bookspace_manager(self):
        """
        Test deleting a author by a bookspace manager.
        """
        book_tag = BookTag.objects.create(name={BookTagChoices.FICTION})
        url = reverse('main:books-detail', kwargs={'pk': book_tag.id})
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Token {self.bookspace_manager_token}')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not BookTag.objects.filter(id=book_tag.id).exists()

    def test_delete_books_as_asst_bookspace_manager(self):
        """
        Test deleting a author by an assistant bookspace manager.
        """
        book_tag = BookTag.objects.create(name={BookTagChoices.FICTION})
        url = reverse('main:books-detail', kwargs={'pk': book_tag.id})
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Token {self.asst_bookspace_manager_token}')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not BookTag.objects.filter(id=book_tag.id).exists()

    def test_delete_books_as_bookspace_worker_permission_denied(self):
        """
        Test deleting a author by a bookspace worker (should be denied).
        """
        book_tag = BookTag.objects.create(name={BookTagChoices.FICTION})
        url = reverse('main:books-detail', kwargs={'pk': book_tag.id})
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Token {self.bookspace_worker_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert BookTag.objects.filter(id=book_tag.id).exists()

    def test_delete_books_as_regular_user_permission_denied(self):
        '''
        Test delete author as a regular user (permission denied)
        '''
        book_tag = BookTag.objects.create(name={BookTagChoices.FICTION})
        url = reverse('main:books-detail', kwargs={'pk': book_tag.id})

        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Token {self.regular_user_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert BookTag.objects.filter(id=book_tag.id).exists()

    def test_delete_books_unauthorized(self):
        '''
        Test delete book by unauthorized request
        '''
        book_tag = BookTag.objects.create(name={BookTagChoices.FICTION})
        url = reverse('main:books-detail', kwargs={'pk': book_tag.id})

        response = self.client.delete(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert BookTag.objects.filter(id=book_tag.id).exists()

    def test_filter_books_by_name(self):
        """
        Test filtering book-tags by name (e.g., get all book-tags with name 'Fiction').
        """
        BookTag.objects.create(name=BookTagChoices.FICTION)
        BookTag.objects.create(name=BookTagChoices.ROMANCE)
        url = reverse('main:books-list')
        url += f'?name=Fiction'

        response = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.bookspace_owner_token}')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['name'] == 'Fiction'

    def test_filter_books_by_partial_name(self):
        """
        Test filtering books by name (e.g., get all book-tags with name 'Fi').
        """

        BookTag.objects.create(name=BookTagChoices.FICTION)
        BookTag.objects.create(name=BookTagChoices.ROMANCE)
        url = reverse('main:books-list')
        url += f'?name=Fi'

        response = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.bookspace_owner_token}')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['name'] == 'Fiction'

    def test_order_books_by_multiple_fields(self):
        """
        Test ordering books by multiple fields (e.g., names in descending order, id in ascending order).
        """
        BookTag.objects.create(name=BookTagChoices.FICTION)
        BookTag.objects.create(name=BookTagChoices.ROMANCE)
        url = reverse('main:books-list')
        url += '?ordering=name'

        response = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.bookspace_manager_token}')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        print(response.data[0]['name'])
        # assert response.data[0]['name'] == 'Fiction'
        # assert response.data[1]['name'] == 'Romance'

    def test_no_results_for_invalid__book_name(self):
        """
        Test filtering with a name that doesn't exist.
        """
        url = reverse('main:books-list')
        url += '?name=nonexistent'
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.bookspace_manager_token}')
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data == {'detail': 'No book tag(s) found matching the provided filters.'}
