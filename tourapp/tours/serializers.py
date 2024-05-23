import cloudinary
from rest_framework import serializers
from .models import (Category, Place, Ticket, Tour, User, CommentInTour,
                     New, Like, Customer, Staff, CommentInNew, Rating, Booking)
from cloudinary.models import CloudinaryField

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CategorySerializerInTour(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class PlaceSerializerInTour(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ['id', 'name']



class PlaceSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(source='image')

    def get_image(self, Place):

        if Place.name:
            public_id = Place.image.public_id
            cloudinary_url = cloudinary.CloudinaryImage(public_id).build_url(folder="imagesOfPlace")
            return cloudinary_url

    class Meta:
        model = Place
        fields = ['id', 'name', 'image']





class TourSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(source='image')
    place = PlaceSerializerInTour(many=True)
    category = CategorySerializerInTour()

    def get_image(self, Tour):

        if Tour.image:
            public_id = Tour.image.public_id
            cloudinary_url = cloudinary.CloudinaryImage(public_id).build_url(folder="imagesOfTour")
            return cloudinary_url

        return None


    class Meta:
        model = Tour
        fields = ['id', 'name', 'category', 'image', 'price_kid', 'price_adult', 'destination',
                  'place']



class NewSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(source='image')


    def get_image(self, New):
        if New.image:
            public_id = New.image.public_id
            cloudinary_url = cloudinary.CloudinaryImage(public_id).build_url(folder="imagesOfNew")
            return cloudinary_url

        return None
    class Meta:
        model = New
        fields = ['id', 'title', 'content', 'image']


class RateSerializer(serializers.ModelSerializer):
    has_rated = serializers.SerializerMethodField()
    tour = TourSerializer()

    def get_has_rated(self, Rating):
        request = self.context.get('request')
        if request.user.is_authenticated:
            tour_id = self.context['request'].data.get('tour_id')
            if tour_id:
                return Rating.user.rating_set.filter(user=request.user).exists()
            else:
                return False
        return False

    class Meta:
        model = Rating
        fields = ['tour', 'user', 'has_rated', 'rate']



class NewDetailSerializer(NewSerializer):
    liked = serializers.SerializerMethodField()


    def get_liked(self, New):
        request = self.context.get('request')
        if request.user.is_authenticated:
            return  New.like_set.filter(active=True).exists()
    class Meta:
        model = New
        fields = NewSerializer.Meta.fields + ['liked']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email', 'avatar']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        data = validated_data.copy()

        user = User(**data)
        user.set_password(data['password'])
        user.save()

        return user


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['first_name', 'last_name', 'username', 'password', 'email', 'is_staff']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        data = validated_data.copy()

        staff = Staff(**data)
        staff.set_password(data['password'])
        staff.save()

        return staff


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'username', 'password', 'email', 'is_staff', 'avatar', 'role']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }


    def create(self, validated_data):
        if 'avatar' not in validated_data or not validated_data['avatar']:
            raise serializers.ValidationError("Avatar is required")

        data = validated_data.copy()
        customer = Customer(**data)
        customer.set_password(data['password'])
        customer.save()
        return customer



class CommentInTourSerializer(serializers.ModelSerializer):
    user = CustomerSerializer()
    class Meta:
        model = CommentInTour
        fields = ['id', 'content', 'user']


class CommentInNewSerializer(serializers.ModelSerializer):
    user = CustomerSerializer()

    class Meta:
        model = CommentInNew
        fields = ['id', 'content', 'user']



class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'option', 'price', 'booking']


class BookingSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True)

    class Meta:
        model = Booking
        fields = ['id', 'customer', 'tour', 'date_depart', 'date_arrive', 'status',
                  'total_price', 'created_at', 'tickets', 'num_adults', 'num_children']

    def create(self, validated_data):
        tickets_data = validated_data.pop('tickets')
        booking = Booking.objects.create(**validated_data)
        for ticket_data in tickets_data:
            Ticket.objects.create(booking=booking, **ticket_data)
        return booking



