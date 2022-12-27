from django.shortcuts import render
from rest_framework.response import Response

# from rest_framework.decorators import action
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status, generics
from .permissions import IsOwner, IsUserOrReadOnly

from .serializers import UserSerializer, ReceiptSerializer, TagSerializer, UserSignupSerializer
from .models import Receipt, Tag
from django.contrib.auth.models import User

class UserSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]

    # def get_permissions(self):
    #     if self.action in ['list', 'create']:
    #         permission_classes = [permissions.AllowAny]
    #     else:
    #         permission_classes = [permissions.IsAuthenticated, IsOwner]
    #     return [permission() for permission in permission_classes]

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

class ReceiptViewSet(viewsets.ModelViewSet):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer

    def get_permissions(self):
        if self.action in ['list', 'create']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated, IsOwner]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [permissions.AllowAny]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]


class UserReceiptViewSet(viewsets.ViewSet):
    def list(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        receipts = Receipt.objects.filter(user=user)
        serializer = ReceiptSerializer(receipts, many=True)
        return Response(serializer.data)


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse("Logged in successfully")
        else:
            return HttpResponse("Invalid login")
    else:
        return HttpResponse("Invalid request method")


def logout(request):
    logout(request)
    return HttpResponse("Logged out successfully")

# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [IsUserOrReadOnly]

# class ReceiptViewSet(viewsets.ModelViewSet):
#     queryset = Receipt.objects.all()
#     serializer_class = ReceiptSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

#     def get_queryset(self):
#         user = self.request.user
#         if user.is_superuser:
#             return Receipt.objects.all()
#         # return Receipt.objects.filter(user=user)
#         return Receipt.objects.all()

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

#     @action(detail=True, methods=['get'])
#     def receipts(self, request, pk=None):
#         receipts = Receipt.objects.filter(user_id=pk)
#         serializer = ReceiptSerializer(
#             receipts, many=True, context={'request': request})
#         return Response(serializer.data)

# class TagViewSet(viewsets.ModelViewSet):
#     queryset = Tag.objects.all()
#     serializer_class = TagSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
