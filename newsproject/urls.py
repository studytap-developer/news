"""newsproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path,include

from rest_framework.routers import DefaultRouter
from newsapp.views import NewsViewSet
router = DefaultRouter()
router.register(r'news', NewsViewSet, basename='news')
from newsapp import views
urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include(router.urls)),
    # Custom endpoints for fetching notifications asynchronously
    # path('api/news/jntuk-notifications/', NewsViewSet.as_view({'get': 'jntuk_notifications'}), name='jntuk_notifications'),
    # path('api/news/jntuh-notifications/', NewsViewSet.as_view({'get': 'jntuh_notifications'}), name='jntuh_notifications'),
    # path('api/news/list-news/', NewsViewSet.as_view({'get': 'list_news'}), name='list_news'),
    # path('api/news/list-tspsc-notifications/', NewsViewSet.as_view({'get': 'list_tspsc_notifications'}), name='list_tspsc_notifications'),
    # path('api/news/jee-notifications/', NewsViewSet.as_view({'get': 'jee_notifications'}), name='jee_notifications'),

]
