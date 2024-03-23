from django.shortcuts import render
from django.http import JsonResponse
from .models import Alert
from .serializers import AlertSerializer, UserSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404  
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
import jwt, datetime 
from rest_framework.exceptions import AuthenticationFailed
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
# Create your views here.

# @cache_page(CACHE_TTL)
@api_view(['GET'])
def alertList(request):
    payload = authFunction(request)
    if request.method == 'GET':
        status = request.GET.get("status", "")
        page_size = request.GET.get("elements", 5)
        if status != "":
            alert = Alert.objects.filter(status=request.GET.get("status"),createdBy=payload['id']).all()
        else:
            alert = Alert.objects.filter(createdBy=payload['id']).all()
                
        paginator = Paginator(alert, page_size)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        alertSerializer = AlertSerializer(page_obj,many =True)
        return Response( alertSerializer.data)
    


@api_view(['POST'])
def alertCreate(request):
    payload = authFunction(request)
    request.data['createdBy'] = payload['id']
    alertSerializer = AlertSerializer(data=request.data)
    if alertSerializer.is_valid():
        alertSerializer.save()
        return Response(alertSerializer.data, status=status.HTTP_201_CREATED)
    


@api_view(['GET', 'PUT'])
def alert_detail(request, id):
    payload = authFunction(request)
    try:
        alert = Alert.objects.get(pk=id,createdBy=payload['id'])
    except Alert.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
        
    if request.method == 'GET':
        alertSerializer = AlertSerializer(alert)
        return Response(alertSerializer.data)
    elif request.method == 'PUT':
        alertSerializer = AlertSerializer(alert,data=request.data)
        if alertSerializer.is_valid():
            alertSerializer.save()
            return Response(alertSerializer.data)
        return Response(alertSerializer.error_messages,status=status.HTTP_400_BAD_REQUEST)    
    


@api_view(['DELETE'])
def alert_delete(request, id):
    payload = authFunction(request)
    try:
        alert = Alert.objects.get(pk=id,createdBy=payload['id'])
    except Alert.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    alert.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)





# user's views

@api_view(['POST'])
def user_signup(request):
    print(request.data)
    userSerializer = UserSerializer(data=request.data)
    print(userSerializer)
    if userSerializer.is_valid():
        userSerializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        return Response(userSerializer.data, status=status.HTTP_201_CREATED)
    return Response(userSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def user_login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"message": "Passord is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
    token, created = Token.objects.get_or_create(user=user)
    userSerializer = UserSerializer(instance=user)
    payload = {
        'id' : user.id,
        'exp': datetime.datetime.now() + datetime.timedelta(minutes=60),
        'iat': datetime.datetime.now()
    }

    token = jwt.encode(payload, 'secret', algorithm='HS256')
    return Response({'token' : token    , 'user' : userSerializer.data})



def authFunction(request):
    token = request.headers.get('Authorization')[7:]
    # print(token)
    if not token:
        raise AuthenticationFailed("Unauthenticated")
    
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("Unauthenticated")
    
    return payload
