from django.shortcuts import render

# Create your views here.
# views.py
from rest_framework import viewsets

from .serializers import UserSerializer, ReceiptSerializer, TagSerializer
from .models import User, Receipt, Tag


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ReceiptView(viewsets.ModelViewSet):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer

class TagView(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
