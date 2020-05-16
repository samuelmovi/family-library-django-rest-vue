from django.urls import path
from django.conf.urls import include
from rest_framework import routers

from .viewsets import LocationViewSet, BookViewSet, LoanViewSet, ActivityViewSet

router = routers.DefaultRouter()

router.register(r'locations', LocationViewSet, basename='locations')
router.register(r'books', BookViewSet, basename='books')
router.register(r'loans', LoanViewSet, basename='loans')
router.register(r'activities', ActivityViewSet, basename='activities')

app_name = 'library'

urlpatterns = [
    path('', include(router.urls)),
]
