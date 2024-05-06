from django.shortcuts import render
from rest_framework import viewsets, generics, status, parsers
from rest_framework.response import Response
from .models import Category, Place, Tour, Ticket, User
from .serializers import CategorySerializer, TourSerializer, PlaceSerializer, UserSerializer
from .paginators import TourPaginator
from  rest_framework.decorators import action



# Create your views here.
class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TourViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    pagination_class = TourPaginator

    def get_queryset(self):
        queries = self.queryset

        q = self.request.query_params.get('q')
        if q:
            queries = queries.filter(name__icontains=q)

        return queries

    @action(methods=['get'], detail=True)
    def places(self, request, pk):
        tour = self.get_object()
        places = tour.place.filter(active=True).all()

        return Response(PlaceSerializer(places, many=True, context={'request': request}).data,
                status=status.HTTP_200_OK)


class PlaceViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = Place.objects.filter(active=True).all()
    serializer_class = PlaceSerializer


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True).all()
    serializer_class = UserSerializer
    parser_classes = [parsers.MultiPartParser]