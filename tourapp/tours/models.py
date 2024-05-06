from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from django import forms
from cloudinary.models import CloudinaryField


class User(AbstractUser):
    avatar = CloudinaryField('avatar', null=True)



class BaseModel(models.Model):
    create_date = models.DateField(auto_now_add=True, null=True)
    updated_date = models.DateField(auto_now=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True

class Category(BaseModel):
    name = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.name


class Place(BaseModel):
    name = models.CharField(max_length=50, null=False)
    description = RichTextField()
    image = models.ImageField(upload_to='Place/name')

    def __str__(self):
        return self.name

class Tour(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, null=True)
    name = models.CharField(max_length=50, null=False)
    description = RichTextField()
    image = models.ImageField(upload_to='Tours/name')
    price_kid = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    price_adult = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    tour_service = models.TextField(null=True)
    place = models.ManyToManyField('Place', related_name='places_tours')
    arrival = models.CharField(max_length=50, null=True)
    department = models.CharField(max_length=50, null=True)


    def __str__(self):
       return self.name


class New(BaseModel):
    title = models.CharField(max_length=255, null=True)
    content = RichTextField()
    author = models.ForeignKey('User', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Ticket(BaseModel):
    OPTIONS_CHOICES = (
        ('A', 'Vé người lớn'),
        ('B', 'Vé trẻ em'),
    )
    option = models.CharField(max_length=1, choices=OPTIONS_CHOICES, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, null=True)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, null=True)
    date_arrive = models.DateField(null=True)
    date_depart = models.DateField(null=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True)
    booking_date = models.DateField(null=True)

    def __str__(self):
        return str(self.id)


class Payment(BaseModel):
    ticket = models.OneToOneField('Ticket', on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=255)
    payment_dated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)