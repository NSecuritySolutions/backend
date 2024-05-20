from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from calculator.views import PriceListView, CalculatorView
from product import views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework import routers
from application.views import ApplicationView

router_v1 = routers.DefaultRouter()
router_v1.register("price-list", PriceListView, basename="price-list")
router_v1.register("calculator", CalculatorView, basename="calculator")
router_v1.register("product", views.ProductListView, basename="product")
router_v1.register("ready", views.ReadySolutionsListView, basename="ready")
router_v1.register("our-service", views.OurServiceListView, basename="our-service")
router_v1.register("our-works", views.OurWorksListView, basename="our-works")
router_v1.register("questions", views.QuestionsListView, basename="questions")


urlpatterns_v1 = [
    path("category/", views.CategoryView.as_view()),
    path("", include(router_v1.urls)),
]

urlpatterns_api = [
    path("v1/", include(urlpatterns_v1)),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger"
    ),
    path(
        "redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"
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