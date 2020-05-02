import random

from django.test import TestCase
from django.test import Client
from django.utils import timezone
from django.urls import reverse
# from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.template.response import TemplateResponse

from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from rest_framework_jwt import utils, views
from rest_framework_jwt.compat import get_user_model
from rest_framework_jwt.settings import api_settings, DEFAULTS

from . import models
from . import factories

# Create your tests here.

User = get_user_model()

credentials = {
    'username': 'test_user',
    'password': 'qwerq32rqwer2q3',
}

def get_auth_token(client):
    # create user
    User.objects.create_user(**credentials)
    # create client
    response = client.post('/auth-jwt/', credentials, format='json')
    return response.data['token']

# MODELS
class LocationTestCase (TestCase):
    test_fields = {
        'address': 'test address',
        'room': 'test room',
        'furniture': "test furniture",
        'details': "test details",
        'username': "test user",
    }
    
    def setUp(self):
        models.Location.objects.create(**self.test_fields)
    
    def test_content(self):
        location = models.Location.objects.get(address="test address")
        for field in self.test_fields:
            self.assertEqual(location.__dict__[field], self.test_fields[field])


class BookTestCase(TestCase):
    test_fields = {
        'title': 'test title',
        'author': 'test author',
        'genre': 'test genre',
        'publisher': 'test publisher',
        'isbn': 'test isbn',
        'publish_date': 'test publish_date',
        'purchase_date': 'test purchase_date',
        'loaned': False,
        'username': 'test username',
    }
    
    def setUp(self):
        models.Location.objects.create(
            address='address',
            room='room',
            furniture='furniture',
            details='details',
            username='test username',
        )
        self.test_fields['location_id'] = models.Location.objects.get(address='address').pk
        models.Book.objects.create(**self.test_fields)
        
    def test_content(self):
        book = models.Book.objects.get(title="test title")
        for field in self.test_fields:
            self.assertEqual(book.__dict__[field], self.test_fields[field])


class LoanTestCase(TestCase):

    book_data = {
        'title': 'test title',
        'author': 'test author',
        'genre': 'test genre',
        'publisher': 'test publisher',
        'isbn': 'test isbn',
        'publish_date': 'test publish_date',
        'purchase_date': 'test purchase_date',
        'loaned': False,
        'username': 'test username',
    }

    test_fields = {
        'book_id': '',
        'lender': 'test lender',
        'borrower': 'test borrower',
    }
    
    def setUp(self):
        models.Book.objects.create(
            title='title',
            author='author',
            genre='genre',
            publisher='publisher',
            isbn='isbn',
            publish_date='publish_date',
            purchase_date='purchase_date',
            location=None,
            loaned=False,
            created=timezone.now(),
            modified=None,
            username='username',
        )
        
        models.Loan.objects.create(
            book=models.Book.objects.get(title='title'),
            lender=self.test_fields['lender'],
            borrower=self.test_fields['borrower'],
        )
    
    def test_content(self):
        loan = models.Loan.objects.get(lender="test lender")
        self.test_fields['book_id'] = models.Book.objects.get(title='title').id
        for field in self.test_fields.keys():
            self.assertEqual(loan.__dict__[field], self.test_fields[field])


# JWT
class JwtTestCase(TestCase):

    auth_data = {
        'username': 'test_user',
        'password': 'qwerq32rqwer2q3',
    }

    def setUp(self):
        # create user
        User.objects.create_user(username=self.auth_data['username'], password=self.auth_data['password'])
        # create client
        self.client = APIClient()

    def test_jwt_get_token_good_creds(self):
        # make request with good creds
        response = self.client.post('/auth-jwt/', self.auth_data, format='json')

        # assert 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # assert response is not null
        self.assertIsNotNone(response)
        # assert response includes token
        self.assertTrue('token' in response.data)
        decoded_payload = utils.jwt_decode_handler(response.data['token'])
        self.assertEqual(decoded_payload['username'], self.auth_data['username'])

    def test_jwt_get_token_bad_creds(self):
        # try to get token with bad credentials
        response = self.client.post('/auth-jwt/', {'username': '1242134', 'password': '123413241'}, format='json')
        # assert 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# ViewSets
class LocationViewSetTest(APITestCase):

    fields = ('address', 'room', 'furniture', 'details')

    def setUp(self):
        self.factory = factories.LocationFactory
        self.model = models.Location
        self.token = get_auth_token(self.client)
    
    def test_not_logged_user_cant_list_locations(self):
        """Not logged-in user can't read notes
        """
        # Create instances
        instances = [self.factory(username=credentials['username']) for n in range(random.randint(1,5))]

        # Request list
        url = '/api/locations/'
        response = self.client.get(url)

        # Assert access is forbidden
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_logged_user_cannot_create_location(self):
        """Not logged-in user cannot create new note
        """
        # Query endpoint
        url = '/api/locations/'
        response = self.client.post(url, data={})

        # Assert access is forbidden
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_logged_user_cannot_modify_existing_location(self):
        """Not logged-in user cannot modify existing note
        """
        # Create instances
        instance = self.factory(username=credentials['username'])

        # Query endpoint
        url = f'/api/locations/{instance.pk}/'
        response = self.client.put(url, {}, format='json')
        
        # Assert forbidden code
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_logged_user_cannot_delete_existing_location(self):
        """Not logged-in user cannot delete existing note
        """
        # Create instances
        instance = self.factory(username=credentials['username'])

        # Query endpoint
        url = f'/api/locations/{instance.pk}/'
        response = self.client.delete(url)
 
        # Assert instance still exists on db
        self.assertTrue(self.model.objects.get(id=instance.pk))

    def test_logged_user_can_list_location(self):
        """Regular logged-in user can list location
        """
        # Create instances
        instances = [self.factory(username=credentials['username']) for n in range(random.randint(1,5))]

        # authorize client
        self.client.credentials(HTTP_AUTHORIZATION='JWT {}'.format(self.token))
        
        # Request list
        url = '/api/locations/'
        response = self.client.get(url)

        # Assert access is allowed
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Assert all instances are returned
        self.assertEqual(len(instances), len(response.data))

    def test_logged_user_can_create_location(self):
        """Regular logged-in user can create location
        """
        # Define request data
        data = {
            'address': 'location address test data',
            'room': 'location room test data',
            'furniture': 'location furniture test data',
            'details': 'location details test data',
        }

        # authorize client
        self.client.credentials(HTTP_AUTHORIZATION='JWT {}'.format(self.token))

        # Query endpoint
        url = '/api/locations/'
        response = self.client.post(url, data=data)

        # Assert endpoint returns created status
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert instance exists on db
        self.assertTrue(self.model.objects.get(id=response.data['id']))
    
    def test_logged_user_can_modify_existing_location(self):
        """Regular logged-in user can modify existing location
        """
        # Create instances
        instance = self.factory(username=credentials['username'])

        # Define request data
        data = {
            'address': 'location address test data MOD',
            'room': 'location room test data MOD',
            'furniture': 'location furniture test data MOD',
            'details': 'location details test data MOD',
        }

        # authorize client
        self.client.credentials(HTTP_AUTHORIZATION='JWT {}'.format(self.token))

        # Query endpoint
        url = f'/api/locations/{instance.pk}/'
        response = self.client.put(url, data, format='json')

        # Assert endpoint returns OK code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert instance has been modified
        for key in data:
            self.assertEqual(data[key], response.data[key])
    
    def test_logged_user_can_delete_existing_location(self):
        """Regular logged-in user can delete existing location
        """
        # Create instances
        instance = self.factory(username=credentials['username'])

        # authorize client
        self.client.credentials(HTTP_AUTHORIZATION='JWT {}'.format(self.token))

        # Query endpoint
        url = f'/api/locations/{instance.pk}/'
        response = self.client.delete(url)

        # Assert 204 no content
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Assert instance not exists anymore on db
        self.assertFalse(self.model.objects.filter(id=instance.pk).exists())


class BookViewSetTest(APITestCase):
    
    def setUp(self):
        self.factory = factories.BookFactory
        self.model = models.Book
        self.token = get_auth_token(self.client)
    
    def test_not_logged_user_cant_list_books(self):
        """Not logged-in user can't read book
        """
        # Create instances
        instances = [self.factory(username=credentials['username']) for n in range(random.randint(1,5))]

        # Request list
        url = '/api/books/'
        response = self.client.get(url)

        # Assert access is forbidden
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_logged_user_cannot_create_book(self):
        """Not logged-in user cannot create new book
        """
        # Query endpoint
        url = '/api/books/'
        response = self.client.post(url, data={})

        # Assert access is forbidden
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_logged_user_cannot_modify_existing_book(self):
        """Not logged-in user cannot modify existing book
        """
        # Create instances
        instance = self.factory(username=credentials['username'])

        # Query endpoint
        url = f'/api/books/{instance.pk}/'
        response = self.client.put(url, {}, format='json')
        
        # Assert forbidden code
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_logged_user_cannot_delete_existing_book(self):
        """Not logged-in user cannot delete existing book
        """
        # Create instances
        instance = self.factory(username=credentials['username'])

        # Query endpoint
        url = f'/api/books/{instance.pk}/'
        response = self.client.delete(url)
 
        # Assert instance still exists on db
        self.assertTrue(self.model.objects.get(id=instance.pk))

    def test_logged_user_can_list_book(self):
        """Regular logged-in user can list book
        """
        # Create instances
        instances = [self.factory(username=credentials['username']) for n in range(random.randint(1,5))]

        # authorize client
        self.client.credentials(HTTP_AUTHORIZATION='JWT {}'.format(self.token))
        
        # Request list
        url = '/api/books/'
        response = self.client.get(url)

        # Assert access is allowed
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Assert all instances are returned
        self.assertEqual(len(instances), len(response.data))

    def test_logged_user_can_create_book(self):
        """Regular logged-in user can create book
        """
        # Define request data
        data = {
            'title': 'book title test data',
            'author': 'book author test data',
            'genre': 'book genre test data',
            'publisher': 'book publisher test data',
            'isbn': 'book title test data',
            'publish_date': 'book publish_date test data',
            'purchase_date': 'book purchase_date test data',
            'location': factories.LocationFactory().pk,
        }

        # authorize client
        self.client.credentials(HTTP_AUTHORIZATION='JWT {}'.format(self.token))

        # Query endpoint
        url = '/api/books/'
        response = self.client.post(url, data=data)

        # Assert endpoint returns created status
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert instance exists on db
        self.assertTrue(self.model.objects.get(id=response.data['id']))
    
    def test_logged_user_can_modify_existing_book(self):
        """Regular logged-in user can modify existing book
        """
        # Create instances
        instance = self.factory(username=credentials['username'])

        # Define request data
        data = {
            'title': 'book title test data MOD',
            'author': 'book author test data MOD',
            'genre': 'book genre test data MOD',
            'publisher': 'book publisher test data MOD',
            'isbn': 'book title test data MOD',
            'publish_date': 'book publish_date test data MOD',
            'purchase_date': 'book purchase_date test data MOD',
            'location': factories.LocationFactory().pk,
        }

        # authorize client
        self.client.credentials(HTTP_AUTHORIZATION='JWT {}'.format(self.token))

        # Query endpoint
        url = f'/api/books/{instance.pk}/'
        response = self.client.put(url, data, format='json')

        # Assert endpoint returns OK code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert not loaned
        self.assertFalse(response.data['loaned'])

        # Assert instance has been modified
        for key in data:
            self.assertEqual(data[key], response.data[key])
    
    def test_logged_user_can_delete_existing_book(self):
        """Regular logged-in user can delete existing book
        """
        # Create instances
        instance = self.factory(username=credentials['username'])

        # authorize client
        self.client.credentials(HTTP_AUTHORIZATION='JWT {}'.format(self.token))

        # Query endpoint
        url = f'/api/books/{instance.pk}/'
        response = self.client.delete(url)

        # Assert 204 no content
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Assert instance not exists anymore on db
        self.assertFalse(self.model.objects.filter(id=instance.pk).exists())


class LoanViewSetTest(APITestCase):
    
    def setUp(self):
        self.factory = factories.LoanFactory
        self.model = models.Loan
        self.token = get_auth_token(self.client)
    
    def test_not_logged_user_cant_list_loans(self):
        """Not logged-in user can't read loan
        """
        # Create instances
        instances = [self.factory(lender=credentials['username']) for n in range(random.randint(1,5))]

        # Request list
        url = '/api/loans/'
        response = self.client.get(url)

        # Assert access is forbidden
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_logged_user_cannot_create_loan(self):
        """Not logged-in user cannot create new loan
        """
        # Query endpoint
        url = '/api/loans/'
        response = self.client.post(url, data={})

        # Assert access is forbidden
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_logged_user_cannot_modify_existing_loan(self):
        """Not logged-in user cannot modify existing loan
        """
        # Create instances
        instance = self.factory(lender=credentials['username'])

        # Query endpoint
        url = f'/api/loans/{instance.pk}/'
        response = self.client.put(url, {}, format='json')
        
        # Assert forbidden code
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_logged_user_cannot_delete_existing_loan(self):
        """Not logged-in user cannot delete existing loan
        """
        # Create instances
        instance = self.factory(lender=credentials['username'])

        # Query endpoint
        url = f'/api/loans/{instance.pk}/'
        response = self.client.delete(url)
 
        # Assert instance still exists on db
        self.assertTrue(self.model.objects.get(id=instance.pk))

    def test_logged_user_can_list_loan(self):
        """Regular logged-in user can list loan
        """
        # Create instances
        instances = [self.factory(lender=credentials['username']) for n in range(random.randint(1,5))]

        # authorize client
        self.client.credentials(HTTP_AUTHORIZATION='JWT {}'.format(self.token))
        
        # Request list
        url = '/api/loans/'
        response = self.client.get(url)

        # Assert access is allowed
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Assert all instances are returned
        self.assertEqual(len(instances), len(response.data))

    def test_logged_user_can_create_loan(self):
        """Regular logged-in user can create loan
        """
        # Define request data
        data = {
            'book': factories.BookFactory().pk,
            'lender': 'test lender data',
            'borrower': 'borrower test data',
        }

        # authorize client
        self.client.credentials(HTTP_AUTHORIZATION='JWT {}'.format(self.token))

        # Query endpoint
        url = '/api/loans/'
        response = self.client.post(url, data=data)

        # Assert endpoint returns created status
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert instance exists on db
        self.assertTrue(self.model.objects.get(id=response.data['id']))
    
    def test_logged_user_can_modify_existing_loan(self):
        """Regular logged-in user can modify existing loan
        """
        # Create instances
        instance = self.factory(lender=credentials['username'])

        # Define request data
        data = {
            'book': instance.book.pk,
            'lender': instance.lender,
            'borrower': instance.borrower,
            # to return book set return_date
            'return_date': timezone.now(),
        }

        # authorize client
        self.client.credentials(HTTP_AUTHORIZATION='JWT {}'.format(self.token))

        # Query endpoint
        url = f'/api/loans/{instance.pk}/'
        response = self.client.put(url, data, format='json')

        # Assert endpoint returns OK code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert instance has been modified
        mod = self.model.objects.get(id=instance.pk)
        self.assertIsNotNone(mod.return_date)
    
    def test_logged_user_cannot_delete_existing_loan(self):
        """Regular logged-in user can delete existing loan
        """
        # Create instances
        instance = self.factory(lender=credentials['username'])

        # authorize client
        self.client.credentials(HTTP_AUTHORIZATION='JWT {}'.format(self.token))

        # Query endpoint
        url = f'/api/loans/{instance.pk}/'
        response = self.client.delete(url)

        # Assert 204 no content
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        # Assert instance not exists anymore on db
        self.assertTrue(self.model.objects.filter(id=instance.pk).exists())
