from django.urls import path,include
from rest_framework import routers
from .views import *
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet,basename='User')

#https://documenter.getpostman.com/view/11807094/UyxjF5ur

urlpatterns = [
    path('', include(router.urls)),
    path('users_create/',views.CreateUserViewSet.as_view({'post': 'create'})),
    path('api-token-auth/', CustomAuthToken.as_view()),
    path('cities/',views.myCities),


    
]

