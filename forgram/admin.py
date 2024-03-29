from django.contrib import admin
from . import models
from django.utils import timezone
from jdatetime import datetime as jdatetime_datetime
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from jdatetime import datetime as jdatetime


admin.site.register(models.ForGramForwarderAdvanceModel)

# admin.site.register(models.ForGramModel)
# admin.site.register(models.ForGramUsersModel)
# admin.site.register(models.ForGramUserMessageModel)
# admin.site.register(models.ForgramPlansModel)
# admin.site.register(models.ForGramRefUsers)
# admin.site.register(models.ForgramUserInvoiceModel)
# admin.site.register(models.ForGramPaymentHistoryModel)
# admin.site.register(models.ForGramSettingModel)
# admin.site.register(models.ForGramUserSession)
# admin.site.register(models.ForGramMessageSenderModel)
# admin.site.register(models.ForGramUserLinkModel)
# admin.site.register(models.ForGramGiftModel)
# admin.site.register(models.ForGramUseGift)









class ForGramUserMessageModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'jalali_created', 'type', 'message_id']
    search_fields = ['user__username']
    list_filter = ['date', 'type']

    def jalali_created(self, obj):
        jalali_date = jdatetime_datetime.fromgregorian(datetime=obj.date).strftime('%Y-%m-%d %H:%M:%S')
        elapsed_time = timezone.now() - obj.date
        elapsed_days = elapsed_time.days
        elapsed_hours, remainder = divmod(elapsed_time.seconds, 3600)
        elapsed_minutes, elapsed_seconds = divmod(remainder, 60)
        return f"{jalali_date} - {elapsed_days} D - {elapsed_hours} H - {elapsed_minutes} M"
    jalali_created.short_description = 'Jalali Created'

admin.site.register(models.ForGramUserMessageModel, ForGramUserMessageModelAdmin)







class ForGramRefUsersAdmin(admin.ModelAdmin):
    list_display = ['inviting_user', 'invited_user', 'jalali_created']
    search_fields = ['inviting_user__username', 'invited_user__username']
    list_filter = ['date']

    def jalali_created(self, obj):
        jalali_date = jdatetime_datetime.fromgregorian(datetime=obj.date).strftime('%Y-%m-%d %H:%M:%S')
        elapsed_time = timezone.now() - obj.date
        elapsed_days = elapsed_time.days
        elapsed_hours, remainder = divmod(elapsed_time.seconds, 3600)
        elapsed_minutes, elapsed_seconds = divmod(remainder, 60)
        return f"{jalali_date} - {elapsed_days} D - {elapsed_hours} H - {elapsed_minutes} M"
    jalali_created.short_description = 'Jalali Created'
admin.site.register(models.ForGramRefUsers, ForGramRefUsersAdmin)



class ForGramUserSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'session_name', 'jalali_created']
    search_fields = ['user__username', 'session_name']
    list_filter = ['created']
    def jalali_created(self, obj):
        jalali_date = jdatetime_datetime.fromgregorian(datetime=obj.created).strftime('%Y-%m-%d %H:%M:%S')
        elapsed_time = timezone.now() - obj.created
        elapsed_days = elapsed_time.days
        elapsed_hours, remainder = divmod(elapsed_time.seconds, 3600)
        elapsed_minutes, elapsed_seconds = divmod(remainder, 60)
        return f"{jalali_date} - {elapsed_days} D - {elapsed_hours} H - {elapsed_minutes} M"
    jalali_created.short_description = 'Jalali Created'
admin.site.register(models.ForGramUserSession, ForGramUserSessionAdmin)





class ForGramUserLinkAdmin(admin.ModelAdmin):
    list_display = ('user', 'forgram', 'link', 'is_complete', 'jalali_created')
    list_filter = ('is_complete',)
    search_fields = ('user__username', 'forgram__name', 'link')
    date_hierarchy = 'created'
    def jalali_created(self, obj):
        jalali_date = jdatetime_datetime.fromgregorian(datetime=obj.created).strftime('%Y-%m-%d %H:%M:%S')
        elapsed_time = timezone.now() - obj.created
        elapsed_days = elapsed_time.days
        elapsed_hours, remainder = divmod(elapsed_time.seconds, 3600)
        elapsed_minutes, elapsed_seconds = divmod(remainder, 60)

        return f"{jalali_date} - {elapsed_days} D - {elapsed_hours} H - {elapsed_minutes} M"
    jalali_created.short_description = 'Jalali Created'
admin.site.register(models.ForGramUserLinkModel, ForGramUserLinkAdmin)







class ForGramSettingAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )
admin.site.register(models.ForGramSettingModel, ForGramSettingAdmin)







class ForgramPlansAdmin(admin.ModelAdmin):
    list_display = ('tag', 'name', 'day', 'volum', 'price', 'discount', 'is_discount', 'is_active')
    search_fields = ('tag', 'name')
    list_filter = ('is_discount', 'is_active')

admin.site.register(models.ForgramPlansModel, ForgramPlansAdmin)




class ForGramPaymentHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'forgram', 'amount', 'is_paid', 'cart_number', 'jalali_request_date')
    list_filter = ('is_paid',)
    search_fields = ('user__username', 'cart_number')
    def jalali_request_date(self, obj):
        jalali_date = jdatetime_datetime.fromgregorian(datetime=obj.request_date).strftime('%Y-%m-%d %H:%M:%S')
        return jalali_date
    jalali_request_date.short_description = 'Request Date'
admin.site.register(models.ForGramPaymentHistoryModel, ForGramPaymentHistoryAdmin)





class ForGramModelAdmin(admin.ModelAdmin):
    list_display = ('username', 'bot_token', 'api_id', 'api_hash')
    search_fields = ('username', 'bot_token', 'api_id', 'api_hash')
    list_per_page = 10  # تعداد آیتم‌های نمایش داده شده در هر صفحه
    list_filter = ('username',)
    ordering = ('-id',)
    fieldsets = (
        ('Main Information', {
            'fields': ('username', 'bot_token', 'api_id', 'api_hash')
        }),
    )
    verbose_name = "Forgram Data"
    verbose_name_plural = "Forgram Data"

admin.site.register(models.ForGramModel, ForGramModelAdmin)




class ForGramGiftModelAdmin(admin.ModelAdmin):
    list_display = ('code', 'count', 'used', 'volum', 'created_jalali', 'days_and_minutes_passed')
    ordering = ('-created',)
    list_filter = ('used', 'forgram')
    search_fields = ('code',)
    verbose_name = "Gift"
    verbose_name_plural = "Gifts"
    def created_jalali(self, obj):
        created_date = timezone.localtime(obj.created)
        jalali_date = jdatetime_datetime.fromgregorian(datetime=created_date).strftime('%Y-%m-%d %H:%M:%S')
        return jalali_date
    created_jalali.short_description = 'Created'
    def days_and_minutes_passed(self, obj):
        delta = timezone.now() - obj.created
        days = delta.days
        minutes = delta.seconds // 60
        return f"{days} days, {minutes} minutes"
    days_and_minutes_passed.short_description = 'Days and Minutes Passed'







@admin.register(models.ForGramUseGift)
class ForGramUseGiftAdmin(admin.ModelAdmin):
    list_display = ('user', 'gift', 'created_jalali', 'days_and_minutes_passed')
    ordering = ('-created',)
    list_filter = ('user__username',)
    search_fields = ('user__username',)
    verbose_name = "Gift Used"
    verbose_name_plural = "Gifts Used"
    def created_jalali(self, obj):
        created_date = timezone.localtime(obj.created)
        jalali_date = jdatetime_datetime.fromgregorian(datetime=created_date).strftime('%Y-%m-%d %H:%M:%S')
        return jalali_date
    created_jalali.short_description = 'Created '
    def days_and_minutes_passed(self, obj):
        delta = timezone.now() - obj.created
        days = delta.days
        minutes = delta.seconds // 60
        return f"{days} days, {minutes} minutes"
    days_and_minutes_passed.short_description = 'Days and Minutes Passed'
admin.site.register(models.ForGramGiftModel, ForGramGiftModelAdmin)











class ForGramUsersAdmin(admin.ModelAdmin):
    list_display = ('user', 'created')
    list_filter = ('created',)
    search_fields = ('user__username', 'forgram__your_field_name')  # جایگزین your_field_name با فیلد مربوطه از مدل ForGramModel
admin.site.register(models.ForGramUsersModel, ForGramUsersAdmin)





class ForGramMessageSenderAdmin(admin.ModelAdmin):
    list_display = ('short_message', 'jalali_created', 'is_completed')
    list_filter = ('created', 'is_completed')
    search_fields = ('message', 'forgram__your_field_name')
    date_hierarchy = 'created'

    def short_message(self, obj):
        return obj.message[:20]

    def jalali_created(self, obj):
        jalali_date = jdatetime_datetime.fromgregorian(datetime=obj.created)
        return f"{jalali_date.strftime('%Y/%m/%d')} {obj.created.strftime('%H:%M:%S')}"
    short_message.short_description = 'Short Message'
    jalali_created.short_description = 'Jalali Created'
admin.site.register(models.ForGramMessageSenderModel, ForGramMessageSenderAdmin)






class PersianDateAdminMixin:
    def jalali_date(self, obj):
        return jdatetime_datetime.fromgregorian(
            year=obj.created_at.year,
            month=obj.created_at.month,
            day=obj.created_at.day,
        ).strftime('%Y/%m/%d')

    jalali_date.short_description = _('Persian Date')
    jalali_date.admin_order_field = 'created_at'


    
class ForgramUserInvoiceModelAdmin(PersianDateAdminMixin, admin.ModelAdmin):
    list_display = ('user', 'plan', 'buyer_user', 'jalali_date', 'paid_at', 'is_paid', 'amount', 'is_discount')
    list_filter = ('is_paid', 'is_discount', 'created_at', 'forgram', 'plan')
    search_fields = ('user__username', 'buyer_user__username', 'notes')
    date_hierarchy = 'created_at' 
    actions = ['mark_as_paid', 'mark_as_unpaid']
    def mark_as_paid(self, request, queryset):
        queryset.update(is_paid='paid', paid_at=timezone.now())
    mark_as_paid.short_description = "Mark selected invoices as paid"
    def mark_as_unpaid(self, request, queryset):
        queryset.update(is_paid='unpaid', paid_at=None)
    mark_as_unpaid.short_description = "Mark selected invoices as unpaid"
admin.site.register(models.ForgramUserInvoiceModel, ForgramUserInvoiceModelAdmin)







class SubForGramUserModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'expiry_jalali', 'time_left_display', 'volum_used', 'is_active')
    list_filter = ('is_active', 'forgram', 'plan')
    search_fields = ('user__username', 'forgram__name')
    date_hierarchy = 'expiry'
    actions = ['activate_selected_subscriptions', 'deactivate_selected_subscriptions']
    def expiry_jalali(self, obj):
        jalali_date = jdatetime.fromgregorian(date=obj.expiry.date())
        return jalali_date.strftime("%Y/%m/%d")
    expiry_jalali.short_description = 'Expiry'
    expiry_jalali.admin_order_field = 'expiry'
    def time_left_display(self, obj):
        time_left = obj.expiry - timezone.now()
        days = time_left.days
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        return f'{days} days, {hours} hours, {minutes} minutes'
    time_left_display.short_description = 'Time Left'
    time_left_display.admin_order_field = 'expiry'
    def activate_selected_subscriptions(self, request, queryset):
        queryset.update(is_active=True)
    activate_selected_subscriptions.short_description = "Activate selected subscriptions"
    def deactivate_selected_subscriptions(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_selected_subscriptions.short_description = "Deactivate selected subscriptions"
admin.site.register(models.SubForGramUserModel, SubForGramUserModelAdmin)
