from django.db import models
from django.contrib.auth.models import AbstractBaseUser
# Create your models here.


class User(AbstractBaseUser):
    pass


class Location(models.Model):
    address = models.CharField(max_length=100)
    room = models.CharField(max_length=100)
    furniture = models.CharField(max_length=100)
    details = models.CharField(max_length=100)
    created = models.DateTimeField('date created', auto_now_add=True)
    username = models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return self.address


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    isbn = models.CharField(max_length=100)
    publish_date = models.CharField(max_length=50)
    purchase_date = models.CharField(max_length=50)
    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING, null=True)
    loaned = models.BooleanField(default=False)
    created = models.DateTimeField('date created', auto_now_add=True)
    modified = models.DateTimeField('date modified', null=True, auto_now=True)
    username = models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return self.title


class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    lender = models.CharField(max_length=100)
    borrower = models.CharField(max_length=100)
    loan_date = models.DateTimeField('date of loan', auto_now_add=True)
    return_date = models.DateTimeField('date of return', null=True)
    
    def __str__(self):
        return self.recipient

