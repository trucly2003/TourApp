import cloudinary
from rest_framework import serializers
from .models import (Category, Place, Ticket, Tour, User, CommentInTour,
                     New, Like, Customer, Staff, CommentInNew)
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
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri('/static/%s' % Place.image.name)
            return '/static/%s' % Place.image.name

    class Meta:
        model = Place
        fields = ['id', 'name', 'image']


class NewSerializer(serializers.ModelSerializer):
    class Meta:
        model = New
        fields = ['']



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
        fields = ['id', 'name', 'category', 'image', 'price_kid', 'price_adult', 'arrival', 'departure',
                  'place']



class NewSerializer(serializers.ModelSerializer):
    class Meta:
        model = New
        fields = ['id', 'title', 'content']


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
        fields = ['first_name', 'last_name', 'username', 'password', 'email', 'avatar']
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
    customer = CustomerSerializer()
    class Meta:
        model = CommentInTour
        fields = ['id', 'content', 'customer']


class CommentInNewSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()

    class Meta:
        model = CommentInNew
        fields = ['id', 'content', 'customer']

