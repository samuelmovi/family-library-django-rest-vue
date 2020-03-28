from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from rest_framework import viewsets, permissions
from rest_framework_jwt.settings import api_settings

from .models import Location, Book, Loan
from .serializers import LocationSerializer, BookSerializer, LoanSerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    # permission_classes = [permissions.AllowAny]
    permission_classes = [permissions.IsAuthenticated]


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # permission_classes = [permissions.AllowAny]
    permission_classes = [permissions.IsAuthenticated]


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    # permission_classes = [permissions.AllowAny]
    permission_classes = [permissions.IsAuthenticated]


@login_required(login_url='/login/')
def default(request):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(request.user)
    token = jwt_encode_handler(payload)
    print("[#] adding token: {}".format(token))
    context = {
    'token': token,
    }
    return render(request, 'library/index.html', context)


