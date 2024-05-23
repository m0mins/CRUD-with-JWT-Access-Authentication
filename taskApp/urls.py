from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenVerifyView
from taskApp import views
from .views import UserRegistrationAPIView,UserLoginAPIView,TodoItemListCreate,TodoItemRetrieveUpdateDestroy

#from rest_framework_simplejwt.views import (
#    TokenRefreshView,
#)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


#router = DefaultRouter()
#router.register(r'todoitems', ToDoTaskAPIView,basename='todoitem')

urlpatterns = [


    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('register/',UserRegistrationAPIView.as_view(),name='register'),
    path('login/',UserLoginAPIView.as_view(),name='login'),
    path('todos/', TodoItemListCreate.as_view(), name='todo-list'),
    path('todos/<int:pk>/', TodoItemRetrieveUpdateDestroy.as_view(), name='todo-detail'),

]