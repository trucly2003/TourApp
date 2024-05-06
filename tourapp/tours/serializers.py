from rest_framework import serializers
from .models import Category, Place, Ticket, Tour, User

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



class TourSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(source='image')
    place = PlaceSerializerInTour(many=True)
    category = CategorySerializerInTour()

    def get_image(self, Tour):

        if Tour.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri('/static/%s' % Tour.image.name)
            return '/static/%s' % Tour.image.name


    class Meta:
        model = Tour
        fields = ['id', 'name', 'category', 'image', 'price_kid', 'price_adult', 'arrival', 'department',
                  'place']


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