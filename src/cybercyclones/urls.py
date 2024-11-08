from django.contrib import admin
from django.http import HttpResponse
from django.urls import path


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
    path('health/', health_check, name='health-check')
]