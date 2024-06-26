"""
URL configuration for loomi_hub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from datetime import datetime

from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from django.conf.urls.static import static

from loomi_hub import settings
from loomi_hub.configuration.openapi import urls_openapi

def index(request):
    now = datetime.now()
    html = f'''
    <html>
        <body>
            <h1>Hello from Loomi HUB!</h1>
            <p>The current time is { now }.</p>
        </body>
    </html>
    '''
    return HttpResponse(html)

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("", index),
        path("user/", include("loomi_hub.user.urls")),
        path("post/", include("loomi_hub.post.urls")),
        path("chat/", include("loomi_hub.chat.urls")),
    ]
    + urls_openapi
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
