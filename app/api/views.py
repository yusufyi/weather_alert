from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer,CitiesSerializer,ProfileSerailzer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from .models import AddCity2,Profile
import requests

# Register User Dont Need Any Auth 
class CreateUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be created.
    """
    queryset = User.objects.all().order_by('-date_joined')
    
    serializer_class = UserSerializer

class UserViewSet(viewsets.ViewSet):
    """
    API endpoint that allows Admin to be deleted or listed.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    
    # List All User
    # Method: GET
    # http://127.0.0.1:8000/users/
    # {Authorization : Token }
    def list (self,request):
        queryset = Profile.objects.all()
        serializer = ProfileSerailzer(queryset, many=True)
        return Response(serializer.data)
    
    # Retrive Individual User
    # Method: GET
    # http://127.0.0.1:8000/users/pk/
    # {Authorization : Token }
    def retrieve(self, request, pk=None):
        print(pk)
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    # Update User
    # Method: PUT
    # http://127.0.0.1:8000/users/pk/
    # {username : password : email}
    def update(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user,request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
    # Delete User
    # Method: DELETE
    # http://127.0.0.1:8000/users/pk/
    # {Authorization : Token }    
    def destroy(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Get Token
# http://127.0.0.1:8000/api-token-auth/
# {username : password} 
class CustomAuthToken(ObtainAuthToken):
  
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })



# ADD ALERT TO USER
@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def myCities(request):
   
    # user = User.objects.filter(id=request.user.id)
    # print(user.username)
    # List exist City For Selected User
    # Method: GET
    # http://127.0.0.1:8000/cities/
    # {Token : Selected User Token }
    if request.method == 'GET':
        objects= AddCity2.objects.all()
        serializer = CitiesSerializer(objects,many=True)
        
        return Response(serializer.data)
    # Add City For Selected User
    # Method: POST
    # http://127.0.0.1:8000/cities/
    # {city  : alertAbove : alertBelow }
    # {Token : Selected User Token }
    elif request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        save_city(request.data['city'],request)
        print(request.data)
        profile = Profile.objects.get(user=user)
        objects = AddCity2.objects.filter(user=profile, city =request.data['city']) 
        serializer = CitiesSerializer(objects,many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# Request Api Endpoint
def get_weather_data(city):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=789bf3b0c057310a46f0da75979330bc'
    api_request = requests.get(url)
    try:
      api_request.raise_for_status()
      return api_request.json()
    except:
      return None

# Save Data to Database after Request Api
def save_city(city,request):
    data = get_weather_data(city)
    user = User.objects.get(id=request.user.id)
    profile = Profile.objects.get(user=user)
  
    AddCity2.objects.update_or_create(user = profile, city = city)
    AddCity2.objects.filter(user = profile, city = city).update(temperatuer=data["main"]["temp"], description=data["weather"][0]["description"]) 
    if request.data['alertAbove']:
        AddCity2.objects.filter(user = profile, city = city).update(alertAbove = request.data['alertAbove'] )
    if request.data['alertBelow']:
        AddCity2.objects.filter(user = profile, city = city).update(alertBelow = request.data['alertBelow'] )


#Check Update weather and check the Alert if its below or Above Send Mail
def updateWeather():
 
    objs = AddCity2.objects.all()
    for obj in objs:
        profile = obj.user
        data = get_weather_data(obj.city)
        user = User.objects.get(id=obj.user.user.id)
        
        city = obj.city
        AddCity2.objects.filter(user = profile, city = city).update(temperatuer=data["main"]["temp"], description=data["weather"][0]["description"])
        if (obj.alertAbove):
            #Check Is There Any Alert
            if obj.alertAbove < data["main"]["temp"]:
                print('alertAbove')
                AddCity2.objects.filter(user = profile, city = city).update(alertAbove=None)
                
                sendMail(user,city,data["main"]["temp"])
        if (obj.alertBelow):
            if obj.alertBelow > data["main"]["temp"]:
                print('alertBelow')
                AddCity2.objects.filter(user = profile, city = city).update(alertBelow=None)
                sendMail(user,city,data["main"]["temp"])

#Send Mail it can be design

def sendMail(user,city,temp):
   
    print(user.email)
    print(f'Alert Email Sent!!!!!')
    print(f'to: {user.email}')
    print(f'{city} new temperatuer:{temp}')
    
    # Need To Set Up Email Settings in The settings.py
    # send_mail(
    # 'Subject here',
    # 'Here is the message.',
    # 'from@example.com',
    # ['to@example.com'],
    # fail_silently=False,)


#Update Weather 
# def updateWeather():
 
#     objs = City.objects.all()
#     for obj in objs:
#         data = get_weather_data(obj.city)
#         user = User.objects.get(id=obj.user.id)
#         city = obj.city
#         City.objects.filter(user = user, city = city).update(temperatuer=data["main"]["temp"], description=data["weather"][0]["description"])
#         #Check Is There Any Alert
#         if (obj.alertAbove):
#             if obj.alertAbove < data["main"]["temp"]:
#                 print('alertAbove')
#                 City.objects.filter(user = user, city = city).update(alertAbove=None)
#                 sendMail(user,city,data["main"]["temp"])
#         if (obj.alertBelow):
#             if obj.alertBelow > data["main"]["temp"]:
#                 print('alertBelow')
#                 City.objects.filter(user = user, city = city).update(alertBelow=None)
#                 sendMail(user,city,data["main"]["temp"])
