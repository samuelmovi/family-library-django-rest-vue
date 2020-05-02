from django.utils import timezone
from django.contrib.gis.geos import Point

from factory import LazyAttribute, SubFactory
from factory.fuzzy import FuzzyText, FuzzyInteger, FuzzyDate, FuzzyDecimal, FuzzyChoice
from factory.django import DjangoModelFactory

from . import models

class LocationFactory(DjangoModelFactory):

    class Meta:
        model = models.Location 
    
    address = FuzzyText(length=80, prefix='address_')
    room = FuzzyText(length=80, prefix='room_')
    furniture = FuzzyText(length=80, prefix='furniture_')
    details = FuzzyText(length=80, prefix='details_')


class BookFactory(DjangoModelFactory):

    class Meta:
        model = models.Book

    title = FuzzyText(length=80, prefix='title_')
    author = FuzzyText(length=80, prefix='author_')
    genre = FuzzyText(length=80, prefix='genre_')
    publisher = FuzzyText(length=80, prefix='publisher_')
    isbn = FuzzyText(length=80, prefix='isbn_')
    publish_date = FuzzyText(length=30, prefix='publish_date_')
    purchase_date = FuzzyText(length=30, prefix='purchase_date_')
    location = SubFactory(LocationFactory)
    loaned = False
    username = "test User"


class LoanFactory(DjangoModelFactory):

    class Meta:
        model = models.Loan

    book = SubFactory(BookFactory)
    lender = FuzzyText(length=80, prefix='lender_')
    borrower = FuzzyText(length=80, prefix='borrower_')

