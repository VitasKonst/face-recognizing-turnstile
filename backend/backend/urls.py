import re
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include
from authentication.backends import JWTAuthentication
from django.contrib.auth.backends import ModelBackend
from django.views.static import serve
from django.conf import settings
from django.shortcuts import HttpResponse
from authentication.models import User


def protected_serve(request, path, document_root=settings.MEDIA_ROOT):
    user = request.user
    if not user.is_staff:
        try:
            auth = JWTAuthentication()
            user = auth.authenticate(request=request)[0]
        except User.DoesNotExist and TypeError:
            return HttpResponse("Sorry you don't have permission to access this file")

    user_portrait_url = user.get_portrait()

    if user_portrait_url == path:
        return serve(request, path, document_root)
    else:
        return HttpResponse("Sorry you don't have permission to access this file")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/authentication/', include('authentication.urls')),
    path('api/v1/', include('main.urls')),
    re_path(r'^%s(?P<path>.*)$' % re.escape(settings.MEDIA_URL.lstrip('/')), protected_serve),
]


