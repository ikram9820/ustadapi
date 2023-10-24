from django.contrib import admin
from . import models

class UserLocationInline(admin.TabularInline):
    model = models.Location


@admin.register(models.Profession)
class ProfessionAdmin(admin.ModelAdmin):
    list_display = ['id','title']
    list_editable = ['title']
    list_per_page = 10
    search_fields = ['title','id']


class UstadOrderInline(admin.TabularInline):
    model = models.Order

@admin.register(models.Ustad)
class UstadAdmin(admin.ModelAdmin):
    inlines = [UstadOrderInline]
    list_display = ['user_id','user','online','rate','profession',]
    search_fields = ['user__username','profession__title']
    list_editable = ['profession']
    list_per_page = 10




class OrderReviewInline(admin.TabularInline):
    model = models.Review

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderReviewInline]
    list_display = ['user','ustad','status','start',]
    list_editable = ['status']
    list_per_page = 10

@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user','order','rate','review']
    list_editable = ['rate','review']
    list_per_page = 10

