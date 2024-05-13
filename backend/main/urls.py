from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from calculator.views import PriceListView
from product import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions, routers
from application.views import ApplicationView

router_v1 = routers.DefaultRouter()
router_v1.register("price-list", PriceListView, basename="price-list")

schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version="v1",
        description="My API description",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="Awesome License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns_v1 = [
    path("product/", views.ProductListView.as_view()),
    path("register/", views.RegisterListView.as_view()),
    path("ready/", views.ReadySolutionsListView.as_view()),
    path("our-service/", views.OurServiceListView.as_view()),
    path("our-works/", views.OurWorksListView.as_view()),
    path("category/", views.CategoryView.as_view()),
    path("questions/", views.QuestionsListView.as_view()),
    path("", include(router_v1.urls)),
]

urlpatterns_api = [
    path("v1/", include(urlpatterns_v1)),
    path(
        "swagger<format>/",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("application/", ApplicationView.as_view()),
    path("application/<int:id>/", ApplicationView.as_view()),
    path("api/", include(urlpatterns_api))
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )