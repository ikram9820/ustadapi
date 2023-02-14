from django.contrib import admin
from . import models

class UserLocationInline(admin.TabularInline):
    model = models.Location

class UstadRangeInline(admin.TabularInline):
    model = models.Range

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name']
    list_editable = ['name']
    list_per_page = 10
    search_fields = ['name','id']


class UstadOrderInline(admin.TabularInline):
    model = models.Order

@admin.register(models.Ustad)
class UstadAdmin(admin.ModelAdmin):
    inlines = [UstadRangeInline,UstadOrderInline]
    list_display = ['user_id','user','status','avr_rating','category',]
    search_fields = ['user__username','category__name']
    list_editable = ['category']
    list_per_page = 10




class OrderReviewInline(admin.TabularInline):
    model = models.Review



@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderReviewInline]
    list_display = ['user','ustad','is_accepted','is_completed','ordered_at',]
    list_editable = ['is_accepted','is_completed']
    list_per_page = 10
@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user','order','rate','review']
    list_editable = ['rate','review']
    list_per_page = 10

