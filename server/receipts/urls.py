from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'receipts', views.ReceiptViewSet)
router.register(r'tags', views.TagViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>', views.UserDetail.as_view()),
    path('users/<int:pk>/receipts/',
         views.UserReceiptViewSet.as_view({'get': 'list'})),
    path('auth/signup/', views.UserSignupView.as_view()),
    path('auth/login/', auth_views.LoginView.as_view()),
    path('auth/logout/', auth_views.LogoutView.as_view()),
]
