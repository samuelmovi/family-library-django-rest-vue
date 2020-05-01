from django.urls import path
from django.conf.urls import url, include
# from . import views
from django.contrib.auth import views as generic_views
from django.views.generic import TemplateView
from rest_framework import routers
from django.conf.urls import url
from rest_framework_simplejwt import views as jwt_views

from .viewsets import LocationViewSet, BookViewSet, LoanViewSet

router = routers.DefaultRouter()

router.register(r'locations', LocationViewSet)
router.register(r'books', BookViewSet)
router.register(r'loans', LoanViewSet)

app_name = 'library'

urlpatterns = [
    path('', include(router.urls)),
]
