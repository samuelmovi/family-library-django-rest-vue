from django.test import TestCase
from django.test import Client
from django.utils import timezone
# from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.template.response import TemplateResponse

from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from rest_framework_jwt import utils, views
from rest_framework_jwt.compat import get_user_model
from rest_framework_jwt.settings import api_settings, DEFAULTS

from .models import Book, Location, Loan
# Create your tests here.

User = get_user_model()

def get_auth_token():
    auth_data = {
        'username': 'test_user',
        'password': 'qwerq32rqwer2q3',
    }
    # create user
    User.objects.create_user(**auth_data)
    # create client
    client = APIClient()
    response = client.post('/auth-jwt/', auth_data, format='json')
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
        Location.objects.create(
            address=self.test_fields['address'],
            room=self.test_fields['room'],
            furniture=self.test_fields['furniture'],
            details=self.test_fields['details'],
            username=self.test_fields['username'],
        )
    
    def test_content(self):
        location = Location.objects.get(address="test address")
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
        'location_id': None,
        'loaned': False,
        'username': 'test username',
    }
    
    def setUp(self):
        Location.objects.create(
            address='address',
            room='room',
            furniture='furniture',
            details='details',
            created=timezone.now(),
            username='username',
        )
        
        Book.objects.create(
            title=self.test_fields['title'],
            author=self.test_fields['author'],
            genre=self.test_fields['genre'],
            publisher=self.test_fields['publisher'],
            isbn=self.test_fields['isbn'],
            publish_date=self.test_fields['publish_date'],
            purchase_date=self.test_fields['purchase_date'],
            location=Location.objects.get(address='address'),
            loaned=self.test_fields['loaned'],
            username=self.test_fields['username'],
        )
        
    def test_content(self):
        book = Book.objects.get(title="test title")
        self.test_fields['location_id'] = Location.objects.get(address='address').id
        for field in self.test_fields:
            self.assertEqual(book.__dict__[field], self.test_fields[field])


class LoanTestCase(TestCase):
    test_fields = {
        'book_id': '',
        'lender': 'test lender',
        'borrower': 'test borrower',
    }
    
    def setUp(self):
        Book.objects.create(
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
        
        Loan.objects.create(
            book=Book.objects.get(title='title'),
            lender=self.test_fields['lender'],
            borrower=self.test_fields['borrower'],
        )
    
    def test_content(self):
        loan = Loan.objects.get(lender="test lender")
        self.test_fields['book_id'] = Book.objects.get(title='title').id
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

class LibraryTestCase(APITestCase):
    string1 = "ewr23rrewfwqe"
    string2 = "pojopi87oijij"
    username1 = 'sam'

    book_fields = {
        'title': string1,
        'author': string1,
        'genre': string1,
        'publisher': string1,
        'isbn': string1,
        'publish_date': string1,
        'purchase_date': string1,
        'loaned': False,
        'username': username1,
    }
    book_fields_mod = {
        'title': string2,
        'author': string2,
        'genre': string2,
        'publisher': string2,
        'isbn': string2,
        'publish_date': string2,
        'purchase_date': string2,
    }
    location_fields = {
        'address': string1,
        'room': string1,
        'furniture': string1,
        'details': string1,
        'username': username1,
    }
    location_fields_mod = {
        'address': string2,
        'room': string2,
        'furniture': string2,
        'details': string2,
    }
    loan_fields = {
        'borrower': 'BOOK_THIEF',
        'lender': username1,
        'book': None,
    }

    def setUp(self):
        self.client = APIClient()
        
        self.token = get_auth_token()

        self.location = Location.objects.create(
            address=self.string2,
            room=self.string2,
            furniture=self.string2,
            details=self.string2,
            username=self.username1,
        )
        self.book = Book.objects.create(
            title=self.string2,
            author=self.string2,
            genre=self.string2,
            publisher=self.string2,
            isbn=self.string2,
            publish_date=self.string2,
            purchase_date=self.string2,
            location=None,
            loaned=False,
            username=self.username1,
        )
        self.loan = Loan.objects.create(
            borrower=self.string1,
            lender=self.string2,
            book=self.book,
        )      

    # BOOK TESTS
    def test_create_book_auth(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT {}'.format(self.token))
        res = self.client.post('/api/books/', data=self.book_fields)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # TODO: assert book has been created
    
    def test_create_book_noauth(self):
        self.client.credentials(HTTP_AUTHORIZATION='')
        res = self.client.post('/api/books/', data=self.book_fields)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_all_books_auth(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT {}'.format(self.token))
        res = self.client.get('/api/books/{}/'.format(self.book.pk))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(len(res.data)>0)
    
    def test_get_all_books_noauth(self):
        self.client.credentials(HTTP_AUTHORIZATION='')
        res = self.client.get('/api/books/{}/'.format(self.book.pk))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_modify_book_auth(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT {}'.format(self.token))
        res = self.client.put('/api/books/{}/'.format(self.book.pk), data=self.book_fields_mod)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # TODO: assert book fields have been modified
    
    def test_modify_book_noauth(self):
        self.client.credentials(HTTP_AUTHORIZATION='')
        res = self.client.put('/api/books/{}/'.format(self.book.pk), data=self.book_fields_mod)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_book_auth(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT {}'.format(self.token))
        res = self.client.delete('/api/books/{}/'.format(self.book.pk))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        # TODO: assert book has been deleted
    
    def test_delete_book_noauth(self):
        self.client.credentials(HTTP_AUTHORIZATION='')
        res = self.client.delete('/api/books/{}/'.format(self.book.pk))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    # LOCATION TESTS
    def test_create_location_auth(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT {}'.format(self.token))
        res = self.client.post('/api/locations/', data=self.location_fields)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # TODO: assert location has been created
    
    def test_create_location_noauth(self):
        self.client.credentials(HTTP_AUTHORIZATION='')
        res = self.client.post('/api/locations/', data=self.location_fields)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_all_location_auth(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT {}'.format(self.token))
        res = self.client.get('/api/locations/{}/'.format(self.location.pk))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(len(res.data)>0)
    
    def test_get_all_location_noauth(self):
        self.client.credentials(HTTP_AUTHORIZATION='')
        res = self.client.get('/api/locations/{}/'.format(self.location.pk))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_modify_location_auth(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT {}'.format(self.token))
        res = self.client.put('/api/locations/{}/'.format(self.location.pk), data=self.location_fields_mod)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # TODO: assert location fields have been modified
    
    def test_modify_location_noauth(self):
        self.client.credentials(HTTP_AUTHORIZATION='')
        res = self.client.put('/api/locations/{}/'.format(self.location.pk), data=self.location_fields_mod)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_location_auth(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT {}'.format(self.token))
        res = self.client.delete('/api/locations/{}/'.format(self.location.pk))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        # TODO: assert location has been deleted

    def test_delete_location_noauth(self):
        self.client.credentials(HTTP_AUTHORIZATION='')
        res = self.client.delete('/api/locations/{}/'.format(self.location.pk))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        
    # LOAN TESTS
    def test_create_loan_auth(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT {}'.format(self.token))
        res = self.client.post('/api/loans/', data={'borrower': 'BOOK_THIEF', 'lender': self.username1, 'book': self.book.pk})
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # TODO: assert loan has been created
    
    def test_create_loan_noauth(self):
        self.client.credentials(HTTP_AUTHORIZATION='')
        res = self.client.post('/api/loans/', data={'borrower': 'BOOK_THIEF', 'lender': self.username1, 'book': self.book.pk})
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_all_loans_auth(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT {}'.format(self.token))
        res = self.client.get('/api/loans/{}/'.format(self.location.pk))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(len(res.data)>0)
    
    def test_get_all_loans_noauth(self):
        self.client.credentials(HTTP_AUTHORIZATION='')
        res = self.client.get('/api/loans/{}/'.format(self.location.pk))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_return_loan_auth(self):
        self.client.credentials(HTTP_AUTHORIZATION='JWT {}'.format(self.token))
        self.loan_fields['returned'] = 'true'
        self.loan_fields['book'] = str(self.book.pk)
        res = self.client.put('/api/loans/{}/'.format(self.loan.pk), data=self.loan_fields)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # TODO: assert loan fields have been modified
    
    def test_return_loan_noauth(self):
        self.client.credentials(HTTP_AUTHORIZATION='')
        self.loan_fields['returned'] = 'true'
        self.loan_fields['book'] = str(self.book.pk)
        res = self.client.put('/api/loans/{}/'.format(self.loan.pk), data=self.loan_fields)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
    
