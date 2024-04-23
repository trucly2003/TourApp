from django.contrib import admin
from .models import Category, Tour, Place

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']

# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tour)
admin.site.register(Place)