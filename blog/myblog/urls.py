from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from .views import *

#app_name = 'myblog'

urlpatterns = [
    path('users/', UserList.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),
    path('users/<int:pk>/profile', UserProfileDetail.as_view()),
    # path('users/<int:pk>/posts', PostList.as_view()),
    path('posts/', PostList.as_view()),
    path('posts/<int:pk>/', PostDetail.as_view()),
    path('posts/<int:pk>/favorite', PostFavoriteView.as_view()),
    path('tags/', TagList.as_view()),
    path('tags/<int:pk>/posts', TagDetailList.as_view()),

    # path('auth/', include('djoser.urls')),
    # path('auth/', include('djoser.urls.authtoken')),
    # path('auth/', include('djoser.urls.jwt')),
    # path('activation/<str:uid>/<str:token>/', ActivateUser.as_view()),
    #path('users/<int:pk>/favorites', UserFavoriteDetail.as_view()),
    #path('posts/<int:pk>/favorites', FavoritesList.as_view()),
    #path('logout/', user_logout, name="logout"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
