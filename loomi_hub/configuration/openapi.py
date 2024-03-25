from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.urls import path

from loomi_hub.configuration.default_schema import BothHttpAndHttpsSchemaGenerator

schema_view = get_schema_view(
    openapi.Info(
        title="loomi Hub API",
        default_version='v1',
        description="Welcome to loomi Hub API Docs",
    ),
    public=True,
    generator_class=BothHttpAndHttpsSchemaGenerator,  # Here
    permission_classes=[permissions.AllowAny],

)

urls_openapi = [
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
