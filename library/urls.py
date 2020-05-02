from django.urls import path
from django.conf.urls import include
from rest_framework import routers

from .viewsets import LocationViewSet, BookViewSet, LoanViewSet

router = routers.DefaultRouter()

router.register(r'locations', LocationViewSet, basename='locations')
router.register(r'books', BookViewSet, basename='books')
router.register(r'loans', LoanViewSet, basename='loans')

app_name = 'library'

urlpatterns = [
    path('', include(router.urls)),
]
