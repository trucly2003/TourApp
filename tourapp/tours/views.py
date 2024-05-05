from django.shortcuts import render
from rest_framework import viewsets, generics
from .models import Category, Place, Tour, Ticket
from .serializers import CategorySerializer, TourSerializer, PlaceSerializer
from .paginators import TourPaginator


# Create your views here.
class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TourViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    pagination_class = TourPaginator


class PlaceViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer