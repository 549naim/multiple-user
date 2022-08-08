from multiprocessing import context
import token
from rest_framework import generics,status
from rest_framework.response import Response
from .serializers import *
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework import permissions
from .permissions import *
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

class FreelancerSignupView(generics.GenericAPIView):
    serializer_class =FreelancerSignupSerializer
    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        user_data=serializer.data
        user =User.objects.get(email=user_data['email'])

        token=RefreshToken.for_user(user).access_token
        
        current_site=get_current_site(request).domain
        relativeLink=reverse('emailverify')
       
        absurl='http://'+current_site+relativeLink+"?token="+str(token)
        email_body='Hi'+user.username+'Use the link for verify your Email \n' + absurl
        data={'email_body':email_body,'to_email':user.email,'email_subject':"Verify your email"}
        Util.send_email(data)
        

        return Response({
            "user":UserSerializer(user,context=self.get_serializer_context()).data,
            "token":Token.objects.get(user=user).key,
            "message":"account created",
        })

class VerifyEmail(generics.GenericAPIView):
    def get(self):
        pass


class ClientSignupView(generics.GenericAPIView):
    serializer_class =ClientSignupSerializer
    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        return Response({
            "user":UserSerializer(user,context=self.get_serializer_context()).data,
            "token":Token.objects.get(user=user).key,
            "message":"account created",
        })


class CustomAuthToken(ObtainAuthToken):
    def post(self,request,*args,**kwargs):
        serializer = self.serializer_class(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        token,created=Token.objects.get_or_create(user=user)
        return Response({
            'token':token.key,
            'user_id':user.pk,
            'is_client':user.is_client
        })

class LogoutView(APIView):
    def post(self, request, format=None):
        request.auth.delete()
        return Response(status=status.HTTP_200_OK)

class ClientOnlyView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated&IsClientUser]
    serializer_class =UserSerializer

    def get_object(self):
        return self.request.user

class FreelancerOnlyView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated&IsFreelancerUser]
    serializer_class =UserSerializer

    def get_object(self):
        return self.request.user        