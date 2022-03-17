from django.shortcuts import render
from rest_framework import mixins
from rest_framework import generics
from api import serializers
from api.models import Product,Purchase
from rest_framework.views import APIView
from api.serializers import UserCreationSerializer,LoginSerializer,PurchaseSerializer
from rest_framework.parsers import MultiPartParser,FormParser
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.contrib.auth import authenticate,login,logout
from rest_framework.authtoken.models import Token
from rest_framework import authentication,permissions

# Create your views here.
class MyProducts(mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 generics.GenericAPIView):
    parser_classes = [MultiPartParser,FormParser]
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)



class RegistrationView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=UserCreationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class Login(APIView):
    def post(self,request,*args,**kwargs):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid():
            username=serializer.validated_data["username"]
            password=serializer.validated_data["password"]
            user=authenticate(request,username=username,password=password)
            if user:
                login(request,user)
                token,created=Token.objects.get_or_create(user=user)
                print(token)
                print(created)
                return Response({"token":token.key},status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class Logout(APIView):
    def get(self,request):
        logout(request)
        return Response({"msg":"session has been ended"})


class Purchases(APIView):
    serializer_class=PurchaseSerializer
    model=Purchase

    def get(self,request,*args,**kwargs):
        purchases=self.model.objects.all()
        serializer=PurchaseSerializer(purchases,many=True)
        return Response(serializer.data)

    def post(self,request,*args,**kwargs):
        serializer=PurchaseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)