from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponseNotAllowed

from rest_framework import viewsets, permissions
from rest_framework_jwt.settings import api_settings
from rest_framework.response import Response

from .models import Location, Book, Loan
from .serializers import LocationSerializer, BookSerializer, LoanSerializer

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'put', 'head']

    # def destroy(self, *args, **kwargs):
    #     return Response(HttpResponseNotAllowed)


# @login_required(login_url='/login/')
def default(request):
    '''
    This view returns the main vuejs-enabled template
    '''
    return render(request, 'library/index.html')
