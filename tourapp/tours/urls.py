
from django.urls import path, re_path, include
from rest_framework import routers
from .views import CategoryViewSet, TourViewSet, PlaceViewSet

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('tours', TourViewSet, basename='tours')
router.register('places', PlaceViewSet, basename='places')


urlpatterns = [
    path('', include(router.urls)),

]
