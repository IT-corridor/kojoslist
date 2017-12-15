# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import *

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'columns', 'column', 'form']
    search_fields = ['name']


class CampCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'column']
    search_fields = ['name']


class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'sortname']
    search_fields = ['name']


class StateAdmin(admin.ModelAdmin):
    list_display = ['name', 'country']
    search_fields = ['name']


class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'state', 'district']
    search_fields = ['name']


class PerkAdmin(admin.ModelAdmin):
    list_display = ['title', 'campaign', 'num_avail']
    search_fields = ['title']


class PerkClaimAdmin(admin.ModelAdmin):
    list_display = ['campaign', 'perk', 'claimer', 'amount', 'transaction']
    search_fields = ['campaign']


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['post', 'rating', 'rater', 'created_at']
    search_fields = ['post']


class PostPurchaseAdmin(admin.ModelAdmin):
    list_display = ['post', 'purchaser', 'type', 'transaction', 'status', 'created_at']
    search_fields = ['post']


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'detail_category', 'category', 'region', 'owner', 'created_at']
    search_fields = ['title', 'category']

    def detail_category(self, obj):
        return '{}/{}'.format(obj.category.parent, obj.category)


class SearchAdmin(admin.ModelAdmin):
    list_display = ['owner', 'category', 'des_state', 'des_city', 'keyword']

    def des_state(self, obj):
        if obj.state:
            return '{} / {}'.format(obj.state.country.name, obj.state.name)

    def des_city(self, obj):
        if obj.city:
            return '{} / {} / {}'.format(obj.city.state.country.name, obj.city.state.name, obj.city.name)


admin.site.register(Customer)
admin.site.register(Review, ReviewAdmin)
admin.site.register(PostPurchase, PostPurchaseAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(GaragePost)
admin.site.register(JobPost)
admin.site.register(CarPost)
admin.site.register(AptPost)
admin.site.register(RoomPost)
admin.site.register(OfficePost)
admin.site.register(BuyGigPost)
admin.site.register(SubletPost)
admin.site.register(RealEstatePost)
admin.site.register(LicensePost)
admin.site.register(Favourite)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Search, SearchAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Image)
admin.site.register(CampCategory, CampCategoryAdmin)
admin.site.register(Campaign)
admin.site.register(Perk, PerkAdmin)
admin.site.register(PerkClaim, PerkClaimAdmin)
