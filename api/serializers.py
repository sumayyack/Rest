from rest_framework.serializers import ModelSerializer
from api.models import Product,Purchase
from django.contrib.auth.models import User
from rest_framework import serializers


class ProductSerializer(ModelSerializer):
    class Meta:
        model= Product
        fields=["product_name","product_image"]


class UserCreationSerializer(ModelSerializer):
    class Meta:
        model=User
        fields=["first_name","email","username","password"]


    def create(self,validated_data):
        return User.objects.create_user(username=validated_data["username"],
                                        email=validated_data["email"],
                                        first_name=validated_data["first_name"],
                                        password=validated_data["password"])

class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()




class PurchaseSerializer(ModelSerializer):
    #product=ProductSerializer(read_only=True)
    class Meta:
        model=Purchase
        fields=["product","purchase_price","selling_price","quantity"]
       # depth=1

    def validate(self, data):
        purchase_price=data['purchase_price']
        selling_price=data['selling_price']
        #quantity=data['quantity']
        if selling_price<purchase_price:
            raise serializers.ValidationError("selling price must be grater than purchase_price")

        return data

    def validate_quantity(self,value):
        if value<0:
            raise serializers.ValidationError("quantity must be greater than zero")
        return value