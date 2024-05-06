from django.contrib import admin
from .models import Category, Tour, Ticket, Place, New
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils.html import mark_safe
from django import forms
from django.urls import path
from django.template.response import TemplateResponse



class TourAppAdminSite(admin.AdminSite):
    site_header = 'Quản lý du lịch'

    def get_urls(self):
        return [
            path('tour-stats/', self.stats_view)
        ] + super().get_urls()

    def stats_view(self, request):
        return TemplateResponse(request, 'admin/stats.html', {
            #sẽ viết một hàm lấy dữ liệu
        })


admin_site = TourAppAdminSite(name='Trang quản lý du lịch')


class NewForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = New
        fields = '__all__'



class TourForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)


    class Meta:
        model = Tour
        fields = '__all__'

class PlaceForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)


    class Meta:
        model = Place
        fields = '__all__'

class PlaceAdmin(admin.ModelAdmin):
    search_fields = ['name']
    form = PlaceForm
    readonly_fields = ['img']

    def img(self, Place):
        if(Place):
            return mark_safe(
                '<img src="/static/{url}" width="120" />' \
                    .format(url=Place.image.name)
           )


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']



class PlaceInline(admin.TabularInline):
    model = Tour.place.through
    extra = 2

class TourAdmin(admin.ModelAdmin):
    search_fields = ['name']
    form = TourForm
    list_display = ['pk','name','category']
    readonly_fields = ['img']
    inlines = [PlaceInline]

    def img(self, tour):
        if (tour):
            return mark_safe(
                '<img src="/static/{url}" width="120" />' \
                    .format(url=tour.image.name)
            )


class TicketForm(forms.ModelForm):


    class Meta:
        model = Ticket
        fields = '__all__'

class TicketAdmin(admin.ModelAdmin):
    form = TicketForm


class NewAdmin(admin.ModelAdmin):
    form = NewForm


# Register your models here.
admin_site.register(Category, CategoryAdmin)
admin_site.register(Tour, TourAdmin)
admin_site.register(Place, PlaceAdmin)
admin_site.register(Ticket, TicketAdmin)
admin_site.register(New, NewAdmin)