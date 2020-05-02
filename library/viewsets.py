from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponseNotAllowed

from rest_framework import viewsets, permissions
from rest_framework_jwt.settings import api_settings
from rest_framework.response import Response

from . import models
from . import serializers

class LocationViewSet(viewsets.ModelViewSet):
    # queryset = Location.objects.all()
    serializer_class = serializers.LocationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return models.Location.objects.filter(username=self.request.user).all()


class BookViewSet(viewsets.ModelViewSet):
    #queryset = Book.objects.all()
    serializer_class = serializers.BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return models.Book.objects.filter(username=self.request.user.username).all()



class LoanViewSet(viewsets.ModelViewSet):
    queryset =models.Loan.objects.all()
    serializer_class = serializers.LoanSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'put', 'head']

    def get_queryset(self):
        return models.Loan.objects.filter(lender=self.request.user.username).all()


# @login_required(login_url='/login/')
def default(request):
    '''
    This view returns the main vuejs-enabled template
    '''
    return render(request, 'library/index.html')
