from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from ckeditor.fields import RichTextField
from django import forms
from cloudinary.models import CloudinaryField


class User(AbstractUser):
    avatar = CloudinaryField('avatar', null=True)
    USER_ROLES = (
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('customer', 'Customer')
    )

    role = models.CharField(max_length=20, choices=USER_ROLES, null=True)



class Customer(User):
    pass


class Admin(User):
    pass


class Staff(User):
    birth = models.DateField(null=True)



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
    image = CloudinaryField('imagesOfPlace', null=True)

    def __str__(self):
        return self.name

class Tour(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, null=True)
    name = models.CharField(max_length=50, null=False)
    destination = models.CharField(max_length=50, null=True)
    description = RichTextField()
    image = CloudinaryField('imagesOfTour', null=True)
    price_kid = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    price_adult = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    tour_service = models.TextField(null=True)
    place = models.ManyToManyField('Place', related_name='places_tours')



class Booking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, null=True)
    num_adults = models.PositiveIntegerField(null=True)
    num_children = models.PositiveIntegerField(null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    date_depart = models.DateField(null=True)
    date_arrive = models.DateField(null=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')], default='Pending', null=True)

    def calculate_return_date(self):
        try:
            nights = int(self.tour.category.name.split('N')[0])
            days = int(self.tour.category.name.split('N')[1].split('Đ')[0])
        except (IndexError, ValueError):
            raise ValueError('Invalid category format')

        return_date = self.date_depart + timedelta(days=nights)
        return return_date

    def __str__(self):
        return f"Booking {self.id} by {self.customer.username}"

class New(BaseModel):
    title = models.CharField(max_length=255, null=True)
    content = models.TextField()
    date_post = models.DateField(auto_now_add=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    image = CloudinaryField('imagesOfNew', null=True)

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
    booking = models.ForeignKey('Booking', on_delete=models.CASCADE,null=True, related_name='tickets')

    def __str__(self):
        return f"Ticket {self.id} for Booking {self.booking.id}"


class Payment(BaseModel):
    ticket = models.OneToOneField('Ticket', on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=255)
    payment_dated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class Interaction(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=False)

    class Meta:
        abstract = True


class CommentInTour(Interaction):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE,null=False)
    content = models.CharField(max_length=255,null=False)

class Rating(Interaction):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE,null=False)
    rate = models.SmallIntegerField(default=0)


class CommentInNew(Interaction):
    new = models.ForeignKey(New, on_delete=models.CASCADE,null=False)
    content = models.CharField(max_length=255, null=False)


class Like(Interaction):
    new = models.ForeignKey(New, on_delete=models.CASCADE,null=False)
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'new')

