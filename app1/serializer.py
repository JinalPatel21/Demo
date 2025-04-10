from rest_framework import serializers
from .models import User, Category, Article
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import update_last_login


class AuthenticationSerializer(serializers.ModelSerializer):
    """This serializer for user authentication"""
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def get_token(self, instance):
        update_last_login(None, instance)
        print(update_last_login(None, instance), 'update last login', instance)
        token = RefreshToken.for_user(instance)
        token.__setitem__("login_time", instance.last_login.timestamp())
        token = token.access_token
        return '{}'.format(token)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    token = serializers.CharField(read_only=True)

    class Meta:
        fields = ['email', 'password', 'token']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = "__all__"
