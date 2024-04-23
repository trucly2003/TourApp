from django.db import models
from django.contrib.auth.models import AbstractUser
from django import forms

class User(AbstractUser):
 pass


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


class Tour(BaseModel):
    name = models.CharField(max_length=50, null=False)
    description = models.TextField()
    image = models.ImageField(upload_to='tours/name')
    price_kid = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    price_adult = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    tour_service = models.TextField(null=True)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, null=True)
    place = models.ManyToManyField('Place')
   # date_arrive = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
   # date_depart = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    def __str__(self):
       return self.name




class Place(BaseModel):
    name = models.CharField(max_length=50, null=False)
    description = models.TextField()
    image = models.ImageField(upload_to='tour/name')

    def __str__(self):
        return self.name


#class ticket(BaseModel):
#   price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
#   datetime_arrive = forms.DateTimeField()
#   datetime_depart = forms.DateTimeField()






