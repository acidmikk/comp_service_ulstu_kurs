from django.contrib import admin
from .models import *


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('image', 'author', 'published')
    search_fields = ('author__username', 'slug')
    date_hierarchy = 'published'
    ordering = ('-published',)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'cost', 'published', 'slug')
    search_fields = ('title', 'slug')
    date_hierarchy = 'published'
    ordering = ('-published',)
    exclude = ('slug',)  # Указываем, какие поля исключить из формы
    prepopulated_fields = {'slug': ('title',)}


class OrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'get_services', 'order_date', 'status', 'check_file')
    list_display_links = ('pk', 'order_date')
    search_fields = ('user__username', 'status')
    date_hierarchy = 'order_date'
    ordering = ('-order_date',)
    exclude = ('slug',)  # Указываем, какие поля исключить из формы
    #prepopulated_fields = {'slug': ('pk',)}

    def get_services(self, obj):
        return ', '.join([service.title for service in obj.services.all()])
    get_services.short_description = 'Услуги'

    def save_model(self, request, obj, form, change):
        if not obj.slug:
            # Создаем slug на основе номера заказа
            obj.slug = slugify(str(obj.pk))
        super().save_model(request, obj, form, change)


admin.site.register(Photo, PhotoAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Order, OrderAdmin)
