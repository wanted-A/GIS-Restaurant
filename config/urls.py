from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="GIS Restaurant API",
        default_version="v1",
        description="위치 기반 음식점 소개 API입니다.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(url="https://github.com/wanted-A/GIS-Restaurant"),
    ),
    public=True,
)

urlpatterns = [
    re_path(
        "^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(r"^$", schema_view.with_ui("swagger", cache_timeout=0), name="schema-root"),
    re_path(
        r"redoc/$",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc-v1",
    ),
    path("admin/", admin.site.urls),
    path("api/v1/users/", include("users.urls")),
    path("api/v1/restaurants/", include("restaurants.urls")),
    path("api/v1/ratings/", include("ratings.urls")),
]
