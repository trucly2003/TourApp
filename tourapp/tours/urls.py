
from django.urls import path, re_path, include
from rest_framework import routers
from .views import CategoryViewSet, TourViewSet, PlaceViewSet, UserViewSet

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('tours', TourViewSet, basename='tours')
router.register('places', PlaceViewSet, basename='places')
router.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('', include(router.urls)),

]
