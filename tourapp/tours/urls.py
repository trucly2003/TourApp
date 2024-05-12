
from django.urls import path, re_path, include
from rest_framework import routers
from .views import (CategoryViewSet, TourViewSet, PlaceViewSet, UserViewSet,
                    TourDetailViewSet, CommentInTourViewSet, NewDetailViewSet, StaffViewSet, CommentInNewViewSet)

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('tours', TourViewSet, basename='tours')
router.register('places', PlaceViewSet, basename='places')
router.register('users', UserViewSet, basename='users')
router.register('staff', StaffViewSet, basename='staff')
router.register('tours', TourDetailViewSet, basename='tour')
router.register('commentsInTour', CommentInTourViewSet, basename='commentsInTour')
router.register('commentsInNew', CommentInNewViewSet, basename='commentsInNew')
router.register('likeInNew', NewDetailViewSet, basename='like')



urlpatterns = [
    path('', include(router.urls)),

]
