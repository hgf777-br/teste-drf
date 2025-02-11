"""
URL configuration for tegge project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from oauth2_provider import urls as oauth2_urls
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import TokenVerifyView, TokenObtainPairView, TokenRefreshView
from knox import views as knox_views
from snippets.views import LoginAPI

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('snippets.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

# Add token authentication endpoint for obtaining tokens for users who want to use the API.
# Default for DRF is to use a POST request with username and password.
urlpatterns += [
    path('api/token/regular/', views.obtain_auth_token, name='token_auth'),
]

# Add token verification endpoint for verifying tokens with Simple JWT.
urlpatterns += [
    path('api/token/jwt/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/jwt/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

# Knox authentication endpoint for obtaining tokens for users who want to use the API.
urlpatterns += [
    path('api/token/knox/login/', LoginAPI.as_view(), name='knox_login'),
    path('api/token/knox/logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('api/token/knox/logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
]

urlpatterns += [
    path('api/token/o/', include(oauth2_urls)),
]