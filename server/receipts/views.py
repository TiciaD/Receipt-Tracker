from django.shortcuts import render
from rest_framework.response import Response

# from rest_framework.decorators import action
# from django.contrib.auth import authenticate, login, logout
# from django.http import HttpResponse
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


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]


class ReceiptViewSet(viewsets.ModelViewSet):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer

    def get_permissions(self):
        if self.action in ['list']:
            permission_classes = [permissions.AllowAny]
        elif self.action in ['create']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated, IsOwner]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['user'] = request.user
        self.perform_create(serializer)

        # Get the list of tags from the request data
        tags = request.data.get('tags')
        if tags:
            tag_names = tags
            # Create a list of Tag objects
            tags = []
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(tag_name=tag_name)
                tags.append(tag)
            # Add the tags to the receipt
            receipt = serializer.instance
            receipt.tags.set(tags)
            receipt.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Get the list of tags from the request data
        tags = request.data.get('tags')
        if tags:
            tag_names = tags
            # Create a list of Tag objects
            tags = []
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(tag_name=tag_name)
                tags.append(tag)
            # Set the tags for the receipt
            instance.tags.set(tags)
            instance.save()
        return Response(serializer.data)


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


# def login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return HttpResponse("Logged in successfully")
#         else:
#             return HttpResponse("Invalid login")
#     else:
#         return HttpResponse("Invalid request method")


# def logout(request):
#     logout(request)
#     return HttpResponse("Logged out successfully")
