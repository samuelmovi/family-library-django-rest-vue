from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers

from .viewsets import LocationViewSet, BookViewSet, LoanViewSet

router = routers.DefaultRouter()

router.register(r'locations', LocationViewSet)
router.register(r'books', BookViewSet)
router.register(r'loans', LoanViewSet)

app_name = 'library'

urlpatterns = [
    url(r'^', include(router.urls))
]
