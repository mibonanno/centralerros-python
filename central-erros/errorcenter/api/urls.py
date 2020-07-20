from django.urls import include, path

from rest_framework import routers
from api import views

app_name = "api"
router = routers.DefaultRouter()
router.register(r'logs', views.LogApiViewSet, basename="logs")
router.register(r'origins', views.OriginApiViewSet, basename="origins")
router.register(r'levels', views.LevelApiViewSet, basename="levels")
router.register(r'users', views.UserApiViewSet, basename="users")

urlpatterns = [
    path('', include(router.urls)),
    path('environments/', views.EnvironmentListOnlyApiView.as_view(), name='environments'),
    path('token/', views.UserToken.as_view(), name="token"),
    path('signup/', views.SignUp),
    path('login/', views.UserToken.user_login, name='login'),
]
