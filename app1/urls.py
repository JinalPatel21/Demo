from django.urls import path
from app1 import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name="user-login"),
    path('access/', views.AccessView.as_view(), name='access-view'),
    path('user/', views.UserRegisterView.as_view(), name='user'),
    path('category/', views.CategoryAPIView.as_view(), name='category'),
    path('article/', views.ArticleAPIView.as_view(), name='article'),
    path("search/articles/", views.ArticleSearchView.as_view(), name="article-search"),
    path("video-call/", views.VideoCallCreateAPIView.as_view()),
]
