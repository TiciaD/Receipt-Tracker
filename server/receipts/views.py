from django.shortcuts import render
from requests import Response

from rest_framework.decorators import action
from rest_framework import viewsets, permissions
from .permissions import IsOwnerOrReadOnly, IsUserOrReadOnly

from .serializers import UserSerializer, ReceiptSerializer, TagSerializer
from .models import Receipt, Tag
from django.contrib.auth.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsUserOrReadOnly]

class ReceiptViewSet(viewsets.ModelViewSet):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Receipt.objects.all()
        # return Receipt.objects.filter(user=user)
        return Receipt.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['get'])
    def receipts(self, request, pk=None):
        receipts = Receipt.objects.filter(user_id=pk)
        serializer = ReceiptSerializer(
            receipts, many=True, context={'request': request})
        return Response(serializer.data)

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
