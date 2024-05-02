"""
URL configuration for main project.

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
from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from calculator.views import *
from product import views
from application.views import ApplicationView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/product/', views.ProductListView.as_view()),
    path('api/v1/register/', views.RegisterListView.as_view()),
    path('api/v1/ready/', views.ReadySolutionsListView.as_view()),
    path('api/v1/our-service/', views.OurServiceListView.as_view()),
    path('api/v1/our-works/', views.OurWorksListView.as_view()),
    path('api/v1/category/', views.CategoryView.as_view()),
    path('api/v1/questions/', views.QuestionsListView.as_view()),


    #Calculator
    path('cal/camera/', CameraView.as_view()),
    path('cal/camera-pr/', CameraPriceView.as_view()),

    #application
    path('application/', ApplicationView.as_view()),
    path('application/<int:id>/', ApplicationView.as_view()),


    #Swagger
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
]
