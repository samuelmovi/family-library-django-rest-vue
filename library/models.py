from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from notifications.signals import notify
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
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(username, password, **extra_fields)


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
        return f'{self.title}'


class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    lender = models.CharField(max_length=100)
    borrower = models.CharField(max_length=100)
    loan_date = models.DateTimeField('date of loan', auto_now_add=True)
    return_date = models.DateTimeField('date of return', null=True)
    
    def __str__(self):
        return f'{self.book} / {self.borrower} / {self.loan_date}'


def book_activity_handler(sender, instance, created, **kwargs):
    #import pdb; pdb.set_trace()
    try:
        owner = User.objects.filter(username=instance.username)[0]
        notify.send(instance, verb='was added')
    except:
        # fail gracefully??
        pass

def location_activity_handler(sender, instance, created, **kwargs):
    notify.send(instance, verb='was added')

def loan_activity_handler(sender, instance, created, **kwargs):
    notify.send(instance, verb='was loaned')

post_save.connect(book_activity_handler, sender=Book)
post_save.connect(location_activity_handler, sender=Location)
post_save.connect(loan_activity_handler, sender=Loan)
