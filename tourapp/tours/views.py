from django.shortcuts import render
from rest_framework import viewsets, generics, status, parsers, permissions, serializers
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from .models import Category, Place, Tour, Rating, Ticket, User, CommentInTour, New, Like, Customer, CommentInNew, Booking
from .serializers import (CategorySerializer, TourSerializer, PlaceSerializer, UserSerializer,
                          CommentInTourSerializer, CommentInNewSerializer, RateSerializer, BookingSerializer,
                          NewSerializer, StaffSerializer, CustomerSerializer, NewDetailSerializer)
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
        if self.action in ['add_comment', 'rate', 'book_tour']:
            return [permissions.IsAuthenticated()]
        return [permission() for permission in self.permission_classes]

    @action(methods=['post'], detail=True, url_path='book_tour')
    def book_tour(self, request, pk=None):
        user = request.user
        tour = self.get_object()
        customer, created = Customer.objects.get_or_create(user_ptr_id=user.id)


        num_adults = request.data.get('num_adults')
        num_children = request.data.get('num_children')
        date_depart = request.data.get('date_depart')

        if not num_adults or not num_children:
            return Response({'error': 'Number of adults and children must be provided'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            num_adults = int(num_adults)
            num_children = int(num_children)
        except ValueError:
            return Response({'error': 'Invalid number of adults or children'}, status=status.HTTP_400_BAD_REQUEST)

        total_price = (tour.price_adult * num_adults) + (tour.price_kid * num_children)

        booking = Booking.objects.create(
            customer=customer,
            tour=tour,
            num_adults=num_adults,
            num_children=num_children,
            total_price=total_price,
            date_depart=date_depart,
            status='pending'
        )
        booking.date_arrive = booking.calculate_return_date()
        booking.save()

        Ticket.objects.bulk_create([
                                       Ticket(option='A', price=tour.price_adult, booking=booking,
                                              category=tour.category) for _ in range(num_adults)
                                   ] + [
                                       Ticket(option='B', price=tour.price_kid, booking=booking, category=tour.category)
                                       for _ in range(num_children)
                                   ])

        serializer = BookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True, url_path='comments')
    def add_comment(self, request, pk=None):
        tour = self.get_object()
        c = CommentInTour.objects.create(user=request.user, tour=tour, content=request.data.get('content'))
        return Response(CommentInTourSerializer(c).data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True, url_path='rate')
    def rate(self, request, pk=None):
        user = request.user
        tour = self.get_object()
        rating = Rating.objects.filter(user=user, tour=tour).first()
        if rating:
            serializer = RateSerializer(rating, context={'request': request})
            return Response(serializer.data)
        rating_value = request.data.get('rate')
        if rating_value:
            rating = Rating.objects.create(user=user, tour=tour, rate=rating_value)
            serializer = RateSerializer(rating, context={'request': request})
            return Response(serializer.data)
        return Response({'message': 'No rate provided'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False, url_path='search_by_price')
    def search_by_price(self, request):
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')
        if min_price is not None and max_price is not None:
            try:
                min_price = float(min_price)
                max_price = float(max_price)
            except ValueError:
                return Response({"error": "Nhập giá trị không đúng"}, status=status.HTTP_400_BAD_REQUEST)
            tours = Tour.objects.filter(price_adult__gte=min_price, price_adult__lte=max_price)
        else:
            tours = Tour.objects.all()
        serializer = TourSerializer(tours, many=True, context={'request': request})
        return Response(serializer.data)

    @action(methods=['get'], detail=False, url_path='search_by_destination')
    def search_by_destination(self, request):
        destination = request.query_params.get('destination')
        if destination:
            tours = Tour.objects.filter(destination__icontains=destination)
            serializer = TourSerializer(tours, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'Hãy nhập thời gian đi hợp lệ'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False, url_path='search_by_duration')
    def search_by_duration(self, request):
        duration = request.query_params.get('duration')
        if not duration:
            return Response({'error': 'Chưa nhập thông tin tra cứu'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            category = Category.objects.get(name=duration)
        except Category.DoesNotExist:
            return Response({'error': 'No category found for the given duration'}, status=status.HTTP_404_NOT_FOUND)

        tours = Tour.objects.filter(category=category)
        serializer = TourSerializer(tours, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class NewDetailViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = New.objects.filter(active=True)
    serializer_class = NewDetailSerializer
    permission_classes = [permissions.AllowAny()]

    def get_permissions(self):
        if self.action in ['like', 'add_comment']:
            return [permissions.IsAuthenticated()]

        return self.permission_classes

    @action(methods=['post'], detail=True, url_path='like')
    def like(self, request, pk):
        like, created = Like.objects.get_or_create(user=request.user, new=self.get_object())
        if not created:
            like.active = not like.active
            like.save()

        serializer = NewDetailSerializer(self.get_object(), context={'request': request})
        return Response(serializer.data,status=status.HTTP_200_OK)

    @action(methods=['post'], url_path='comments', detail=True)
    def add_comment(self, request, pk):
        c = CommentInTour.objects.create(user=request.user, tour=self.get_object(), content=request.data.get('content'))

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
        if self.action in ['current_user']:
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



class BookingViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action in ['add_tickets', 'confirm']:
            return [permissions.IsAuthenticated()]
        return  self.permission_classes

    # def create_booking(self, request):
    #     data = request.data
    #     serializer = BookingSerializer(data=data)
    #     if serializer.is_valid():
    #         booking = serializer.save(user=request.user)
    #
    #         # Tạo các ticket tương ứng
    #         num_adults = data.get('adults', 0)
    #         num_children = data.get('kids', 0)
    #
    #         for _ in range(num_adults):
    #             Ticket.objects.create(
    #                 option='A',
    #                 price=booking.tour.price_adult,
    #                 tour=booking.tour,
    #                 booking=booking,
    #                 user=request.user,
    #                 date_arrive=booking.tour.arrival_date,
    #                 date_depart=booking.tour.departure_date
    #             )
    #
    #         for _ in range(num_children):
    #             Ticket.objects.create(
    #                 option='B',
    #                 price=booking.tour.price_child,
    #                 tour=booking.tour,
    #                 booking=booking,
    #                 user=request.user,
    #                 date_arrive=booking.tour.arrival_date,
    #                 date_depart=booking.tour.departure_date
    #             )
    #
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @action(methods=['get'], detail=False, url_path='my_bookings')
    # def my_bookings(self, request):
    #     bookings = Booking.objects.filter(user=request.user)
    #     serializer = BookingSerializer(bookings, many=True)
    #     return Response(serializer.data)

class CommentInTourViewSet(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = CommentInTour.objects.all()
    serializer_class = CommentInTourSerializer
    permission_classes = [OwnerAuthenticated]

class CommentInNewViewSet(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = CommentInNew.objects.all()
    serializer_class = CommentInNewSerializer
    permission_classes = [OwnerAuthenticated]


