from django.db import models
from django.db.models.signals import post_save, post_delete, pre_save
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.


# User Manager
class CustomUserManager(BaseUserManager):

    def create(self, username, password, **extra_fields):
        return self.create_user(username, password, **extra_fields)

    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError(_('The username must be set'))
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        user = self.create_user(username, password, **extra_fields)
        user.is_active = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser):

    username = models.CharField(max_length=100, unique=True)
    email = None

    objects = CustomUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.username}'


class Location(models.Model):
    address = models.CharField(max_length=100)
    room = models.CharField(max_length=100)
    furniture = models.CharField(max_length=100)
    details = models.CharField(max_length=100)
    created = models.DateTimeField('date created', auto_now_add=True)
    username = models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return f'{self.address}'


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
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='book_owner', null=True)
    
    def __str__(self):
        return f'{self.title}, by {self.author}'


class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    lender = models.CharField(max_length=100)
    borrower = models.CharField(max_length=100)
    loan_date = models.DateTimeField('date of loan', auto_now_add=True)
    return_date = models.DateTimeField('date of return', null=True)
    
    def __str__(self):
        return f'{self.book} / {self.borrower} / {self.loan_date}'

class Activity(models.Model):

    actor = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='activity')
    verb = models.CharField(max_length=100)
    book = models.ForeignKey(Book, on_delete=models.DO_NOTHING, related_name='activity', null=True)
    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING, related_name='activity', null=True)
    recipient = models.CharField(max_length=100, null=True)

    def __str__(self):
        if self.recipient is not None:
            return f'{self.actor} loaned {self.book}, to {self.recipient}' 
        if self.book is not None and self.location is not None:
            return f'{self.actor} moved {self.book}, to {lself.ocation}'
        if self.book is not None:
            return f'{self.actor} {self.verb} {self.book}'
        if self.location is not None:
            return f'{self.actor} {self.verb} {self.location}'

def book_save_handler(sender, instance, created, **kwargs):
    try:
        owner = User.objects.filter(username=instance.username)[0]
        Activity.objects.create(actor=owner, verb='added book', book=instance)
    except:
        # fail gracefully??
        pass

def book_deletion_handler(sender, instance, created, **kwargs):
    try:
        owner = User.objects.filter(username=instance.username)[0]
        Activity.objects.create(actor=owner, verb='deleted', book=instance)
    except:
        # fail gracefully??
        pass

def location_save_handler(sender, instance, created, **kwargs):
    try:
        owner = User.objects.filter(username=instance.username)[0]
        Activity.objects.create(actor=owner, verb='added new location', location=instance)
    except:
        # fail gracefully??
        pass

def location_deletion_handler(sender, instance, created, **kwargs):
    try:
        owner = User.objects.filter(username=instance.username)[0]
        Activity.objects.create(actor=owner, verb='deleted', location=instance)
    except:
        # fail gracefully??
        pass

# def loan_save_handler(sender, instance, created, **kwargs):
#     try:
#         owner = User.objects.filter(username=instance.username)[0]
#         book = Book.objects.filter(id = instance.book.id)
#         Activity.objects.create(actor=owner, verb='loaned', book=book, recipient=instance.recipient)
#     except:
#         # fail gracefully??
#         pass

# def loan_returned_handler(sender, instance, created, **kwargs):
#     try:
#         owner = User.objects.filter(username=instance.username)[0]
#         book = Book.objects.filter(id = instance.book.id)
#         Activity.objects.create(actor=owner, verb='returned', book=book, recipient=instance.recipient)
#     except:
#         # fail gracefully??
#         pass

post_save.connect(book_save_handler, sender=Book)
post_delete.connect(book_deletion_handler, sender=Book)

post_save.connect(location_save_handler, sender=Location)
post_delete.connect(location_deletion_handler, sender=Loan)
