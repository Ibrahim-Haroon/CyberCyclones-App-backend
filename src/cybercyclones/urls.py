from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from rest_framework import routers
from src.rest.auth_controller import AuthController
from src.rest.discovery_controller import DiscoveryController
from src.rest.leaderboard_controller import LeaderboardController
from src.rest.points_controller import PointsController
from src.rest.skin_controller import SkinController
from src.rest.user_controller import UserController

router = routers.DefaultRouter()

router.register(r'auth', AuthController, basename='auth')
router.register(r'discoveries', DiscoveryController, basename='discoveries')
router.register(r'leaderboard', LeaderboardController, basename='leaderboard')
router.register(r'points', PointsController, basename='points')
router.register(r'skins', SkinController, basename='skins')
router.register(r'users', UserController, basename='users')


def root_view(request) -> HttpResponse:
    """
    @rtype: HttpResponse
    @param request: request object (unused)
    @return: 200 for healthy, 500 for unhealthy
    """
    try:
        return HttpResponse("Hello! You're at the root of the Cyber Clones server.", status=200)
    except Exception as e:
        return HttpResponse(f"error: {str(e)}", status=500)


def health_check(request) -> HttpResponse:
    """
    :rtype: HttpResponse
    :param request: request object (unused)
    :return: 200 for healthy, 500 for unhealthy
    """
    try:
        return HttpResponse(status=200)
    except Exception as e:
        return HttpResponse(f"error: {str(e)}", status=500)


urlpatterns = [
    path('', root_view, name='root'),
    path('admin/', admin.site.urls),
    path('health/', health_check, name='health-check'),
    path('api/v1/', include(router.urls))
]
