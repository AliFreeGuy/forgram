from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group
from .models import User
from django.utils import timezone
from jdatetime import datetime as jdatetime_datetime

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'phone_number', 'full_name', 'creation_time_since',  'is_active')
    list_filter = ('is_admin', 'creation')
    fieldsets = (
        (None, {'fields': ('username', 'phone_number', 'full_name', 'password', 'cart_number')}),
        ('Permissions', {'fields': ('is_active', 'is_admin', 'last_login')}),
    )
    add_fieldsets = (
        (None, {'fields': ('username', 'phone_number', 'full_name', 'password1', 'password2')}),
    )
    search_fields = ('username', 'full_name', 'phone_number')
    ordering = ('-creation',)
    filter_horizontal = ()


    def creation_time_since(self, obj):
        jalali_date = jdatetime_datetime.fromgregorian(datetime=obj.creation)
        jalali_creation= f"{jalali_date.strftime('%Y/%m/%d')} {obj.creation.strftime('%H:%M:%S')}"
        time_since_creation = timezone.now() - obj.creation
        minutes_since_creation = int(time_since_creation.total_seconds() / 60)
        if minutes_since_creation < 60:
            return f'{jalali_creation} - {minutes_since_creation} min ago'
        hours_since_creation = int(time_since_creation.total_seconds() / 3600)
        if hours_since_creation < 24:
            return f'{jalali_creation} - {hours_since_creation} hours ago'
        days_since_creation = int(time_since_creation.total_seconds() / 86400)
        return f'{jalali_creation} - {days_since_creation} day ago'
    creation_time_since.short_description = 'creation'
    creation_time_since.admin_order_field = 'creation'

        


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
