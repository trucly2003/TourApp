from django.contrib import admin
from .models import Category, Tour, Ticket, Place, New, User
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils.html import mark_safe
from django import forms
from django.urls import path
from django.template.response import TemplateResponse
from django.contrib.auth.hashers import make_password



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


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'is_active',
                  'is_staff', 'avatar', 'role']

class PlaceAdmin(admin.ModelAdmin):
    search_fields = ['name']
    form = PlaceForm


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']


class UserAdmin(admin.ModelAdmin):
    form = UserForm

    def password(self, request, obj, form, change):
        obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)


class PlaceInline(admin.TabularInline):
    model = Tour.place.through
    extra = 2

class TourAdmin(admin.ModelAdmin):
    search_fields = ['name']
    form = TourForm
    list_display = ['pk','name','category']
    inlines = [PlaceInline]


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
admin_site.register(User, UserAdmin)