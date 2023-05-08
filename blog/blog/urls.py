from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

#from myblog.views import ActivateUser

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myblog.urls')),
    path('api-auth/', include('rest_framework.urls')),  # ДОБАВЛЯЕМ КНОПОЧКУ LOG IN В UI
    path('auth/', include('djoser.urls')),
    #path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt')),
    #path('auth/activation/<uid>/<token>', ActivateUser.as_view({'get': 'activation'}), name='activation'),
    #path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
