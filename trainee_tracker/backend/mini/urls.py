from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MiniProjectViewSet, UserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'projects', MiniProjectViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_project, name="create_project"),
    path("<int:pk>/update/", views.update_project, name="update_project"),
    path("<int:pk>/delete/", views.delete_project, name="delete_project"),
]
