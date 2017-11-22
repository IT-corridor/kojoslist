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
	list_display = ['name', 'state']
	search_fields = ['name']

class SearchAdmin(admin.ModelAdmin):
	list_display = ['owner', 'category', 'des_state', 'des_city', 'keyword']

	def des_state(self, obj):
		if obj.state:
			return '{} / {}'.format(obj.state.country.name, obj.state.name)

	def des_city(self, obj):
		if obj.city:
			return '{} / {} / {}'.format(obj.city.state.country.name, obj.city.state.name, obj.city.name)

admin.site.register(Customer)
admin.site.register(Post)
admin.site.register(GaragePost)
admin.site.register(JobPost)
admin.site.register(Favourite)
admin.site.register(Hidden)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Search, SearchAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Image)
admin.site.register(CampCategory, CampCategoryAdmin)
