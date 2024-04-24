from django.contrib import admin
from .models import Category, Tour, Place, Ticket
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms


class TourForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)


    class Meta:
        model = Tour
        fields = '__all__'


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']

class TourAdmin(admin.ModelAdmin):
    search_fields = ['name']
    form = TourForm
    list_display = ['pk','name']

class TicketForm(forms.ModelForm):
    date_arrive = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time_arrive = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    date_depart = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time_depart = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    class Meta:
        model = Ticket
        fields = '__all__'

class TicketAdmin(admin.ModelAdmin):
    form = TicketForm

# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tour, TourAdmin)
admin.site.register(Place)
admin.site.register(TicketAdmin, TicketForm)