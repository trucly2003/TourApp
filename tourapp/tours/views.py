from django.shortcuts import render
from rest_framework import viewsets, generics, status, parsers, permissions
from rest_framework.response import Response
from .models import Category, Place, Tour, Ticket, User, CommentInTour, New, Like, Staff, CommentInNew
from .serializers import (CategorySerializer, TourSerializer, PlaceSerializer, UserSerializer,
                          CommentInTourSerializer, CommentInNewSerializer,
                          NewSerializer, StaffSerializer, CustomerSerializer)
from .paginators import TourPaginator
from  rest_framework.decorators import action
from .perms import OwnerAuthenticated, IsSuperUser



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



class PlaceViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Place.objects.filter(active=True).all()
    serializer_class = PlaceSerializer


class TourDetailViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = Tour.objects.filter(active=True).all()
    serializer_class = TourSerializer
    permission_classes = [permissions.AllowAny]


    def get_permissions(self):
        if self.action in ['add_comment']:
            return [permissions.IsAuthenticated()]

        return self.permission_classes

    @action(methods=['post'], url_path='comments', detail=True)
    def add_comment(self, request, pk):
        c = CommentInTour.objects.create(customer=request.customer, tour=self.get_object(), content=request.data.get('content'))

        return Response(CommentInTourSerializer(c).data, status=status.HTTP_201_CREATED)


class NewDetailViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = New.objects.filter(active=True)
    serializer_class = NewSerializer
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        if self.action in ['Like', 'add_comment']:
            return [permissions.IsAuthenticated()]

        return self.permission_classes

    @action(methods=['post'], detail=True, url_path='Like')
    def Like(self, request, pk):
        like, created = Like.objects.create_or_update(user=request.user, new=self.get_object())
        if not created:
            like.active = not like.active
            like.save()

        return Response(status=status.HTTP_201_OK)

    @action(methods=['post'], url_path='comments', detail=True)
    def add_comment(self, request, pk):
        c = CommentInTour.objects.create(customer=request.customer, tour=self.get_object(), content=request.data.get('content'))

        return Response(CommentInTourSerializer(c).data, status=status.HTTP_201_CREATED)


class StaffViewSet(viewsets.ViewSet):
    queryset = User.objects.filter(is_active=True).all()
    serializer_class = StaffSerializer
    permission_classes = [permissions.AllowAny]


    def get_permissions(self):
        if self.action in ['add_employee']:
            return [permissions.IsAdminUser()]
        return self.permission_classes

    @action(methods=['post'], detail=False, url_name='add_employee')
    def add_employee(self, request):
         if request.user.is_superuser:
             serializer = self.serializer_class(data=request.data)
             if serializer.is_valid():
                 serializer.save()
                 return Response(serializer.data, status=status.HTTP_201_CREATED)
             else:
                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ViewSet):
    queryset = User.objects.filter(is_active=True).all()
    serializer_class = UserSerializer


    def get_permissions(self):
        if self.action.__eq__('current_user'):
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]


    @action(methods=['post'], detail=False)
    def register_customer(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(methods=['get'], detail=False, url_name='current_user')
    def current_user(self, request):
        return Response(UserSerializer(request.user).data)





class CommentInTourViewSet(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = CommentInTour.objects.all()
    serializer_class = CommentInTourSerializer
    permission_classes = [OwnerAuthenticated]

class CommentInNewViewSet(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = CommentInNew.objects.all()
    serializer_class = CommentInNewSerializer
    permission_classes = [OwnerAuthenticated]