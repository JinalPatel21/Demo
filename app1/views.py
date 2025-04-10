from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .documents import ArticleDocument
from .serializer import LoginSerializer, AuthenticationSerializer, CategorySerializer, ArticleSerializer, UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User, Category, Article
import requests
from .utils import generate_videosdk_token
from rest_framework import viewsets


class LoginView(APIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.get(email__iexact=serializer.data.get('email'))
            data = AuthenticationSerializer(user, context={"request": self.request}).data

            if not user.check_password(request.data['password']):
                error = {"password": "invalid credentials"}
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
            elif not user.is_active:
                error = {"email": "your account is deactivated  . please contact support team"}
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            error = {'email': "this email is not registered in system"}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)


class AccessView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = "this is my accessible credentials"
            return Response(user, status=status.HTTP_200_OK)

        except Exception as e:
            error = 'this is my invalid credentials'
            return Response(error, status=status.HTTP_400_BAD_REQUEST)


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return User.objects.all()


class CategoryAPIView(generics.CreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Category.objects.all()


class ArticleAPIView(generics.CreateAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Article.objects.all()

class ArticleSearchView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.GET.get('q', '')

        results = ArticleDocument.search().query(
            "multi_match",
            query=query,
            fields=['title^2', 'content', 'author.first_name', 'categories.name'],
            fuzziness='AUTO'
        )

        data = []
        for hit in results:
            categories_data = []
            if isinstance(hit.categories, list):
                for cat in hit.categories:
                    if isinstance(cat, dict) and "name" in cat:
                        categories_data.append(cat["name"])

            data.append({
                "title": hit.title,
                "content": hit.content,
                "author": hit.author["first_name"] if isinstance(hit.author, dict) else None,
                "categories": categories_data
            })

        return Response(data)


def create_meeting():
    token = generate_videosdk_token()
    url = "https://api.videosdk.live/v2/rooms"

    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers)
    return response.json(), token


class VideoCallCreateAPIView(APIView):
    def get(self, request):
        room_data, token = create_meeting()
        return Response({
            "roomId": room_data.get("roomId"),
            "token": token
        })
