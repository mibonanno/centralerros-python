"""errorcenter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from api import urls, views

from django.views.generic.base import TemplateView

app_name='api'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(('api.urls','api'), namespace='api')),
    path('logs/', views.LogsList.as_view(), name='logs'),
    path(r'logs/delete/', views.LogDeleteList, name='logs-delete-list'),
    path(r'logs/<int:pk>/delete/', views.LogDelete.as_view(), name='logs-delete'),
    path(r'logs/<int:pk>/archive/', views.LogArchive.as_view(), name='logs-archive'),
    path(r'', include('django.contrib.auth.urls')),
]
