from django.db import models
from django.contrib.auth.models import AbstractUser


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


class

class Tour(BaseModel):
    name = models.CharField(max_length=50, null=False)
    description = models.TextField()
    image = models.ImageField(upload_to='tours/name')
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, null=True)
    price_kid = models.CharField(max_length=20, null=False)
    price_adult = models.CharField(max_length=20, null=False)


    def __str__(self):
        return self.name