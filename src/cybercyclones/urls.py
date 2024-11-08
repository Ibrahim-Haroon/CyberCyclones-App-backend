from django.contrib import admin
from django.http import HttpResponse, JsonResponse
from django.urls import path


def root_view(request) -> HttpResponse:
    """
    @rtype: HttpResponse
    @param request: request object
    @return: response for root view
    """
    try:
        return HttpResponse("Hello! You're at the root of the Cyber Clones server.", status=200)
    except Exception as e:
        return HttpResponse(f"error: {str(e)}", status=500)


def health_check(request) -> HttpResponse:
    """
    :rtype: JsonResponse
    :param request: request object
    :return: response for health check
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