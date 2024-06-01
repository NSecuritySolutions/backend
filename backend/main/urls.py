from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework import routers

from application.views import ApplicationView
from calculator.views import CalculatorView, PriceListView
from product.views import (
    CategoryView,
    OurServiceListView,
    OurWorksListView,
    ProductListView,
    ReadySolutionsListView,
)
from social.views import QuestionsListView, TeamListView

router_v1 = routers.DefaultRouter()
router_v1.register("price-list", PriceListView, basename="price-list")
router_v1.register("calculator", CalculatorView, basename="calculator")
router_v1.register("products", ProductListView, basename="product")
router_v1.register("ready-solutions", ReadySolutionsListView, basename="ready")
router_v1.register("our-services", OurServiceListView, basename="our-service")
router_v1.register("our-works", OurWorksListView, basename="our-works")
router_v1.register("questions", QuestionsListView, basename="questions")
router_v1.register("our-team", TeamListView, basename="our-team")


urlpatterns_v1 = [
    path("category/", CategoryView.as_view()),
    path("", include(router_v1.urls)),
]

urlpatterns_api = [
    path("v1/", include(urlpatterns_v1)),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("application/", ApplicationView.as_view()),
    path("application/<int:id>/", ApplicationView.as_view()),
    path("api/", include(urlpatterns_api)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
