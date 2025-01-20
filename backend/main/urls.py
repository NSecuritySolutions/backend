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

from application.views import (
    ApplicationListView,
    ApplicationWithCalcView,
    ApplicationWithFileView,
    ApplicationWithSolutionView,
    set_csrf_token,
)
from calculator.views import CalculatorView
from product.views import (
    NewProductListView,
    OurServiceListView,
    OurWorksListView,
    ProductListView,
    ReadySolutionsListView,
    TagListView,
    api_view_test,
)
from social.views import (
    OurGuaranteesView,
    QuestionsListView,
    ReviewsView,
    SocialInfoView,
    TeamListView,
)

router_v1 = routers.DefaultRouter()
router_v1.register(
    "calc-applications", ApplicationWithCalcView, basename="calc-applications"
)
router_v1.register(
    "solution-applications",
    ApplicationWithSolutionView,
    basename="solution-applications",
)
router_v1.register(
    "simple-applications", ApplicationWithFileView, basename="file-applications"
)
router_v1.register("applications", ApplicationListView, basename="applications")
router_v1.register("calculator", CalculatorView, basename="calculator")
router_v1.register("products", ProductListView, basename="product")
router_v1.register("new-products", NewProductListView, basename="new-product")
router_v1.register("ready-solutions", ReadySolutionsListView, basename="ready")
router_v1.register("solutions-tags", TagListView, basename="solution-tags")
router_v1.register("our-services", OurServiceListView, basename="our-service")
router_v1.register("our-works", OurWorksListView, basename="our-works")
router_v1.register("questions", QuestionsListView, basename="questions")
router_v1.register("our-team", TeamListView, basename="our-team")
router_v1.register("info", SocialInfoView, basename="info")
router_v1.register("guarantees", OurGuaranteesView, basename="guarantees")
router_v1.register("reviews", ReviewsView, basename="reviews")


urlpatterns_v1 = [
    path("test", api_view_test),
    path("set-csrf-token/", set_csrf_token),
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
    # path("application/", ApplicationView.as_view()),
    # path("application/<int:id>/", ApplicationView.as_view()),
    path("api/", include(urlpatterns_api)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
