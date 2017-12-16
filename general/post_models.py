# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from .models import Post

EMPLOYMENT_TYPE = [
    ('full-time', 'full-time'), 
    ('part-time', 'part-time'), 
    ('contract', 'contract'), 
    ("employee's choice", "employee's choice")
]

class JobPost(Post):
    employment_type = models.CharField(choices=EMPLOYMENT_TYPE, max_length=50)
    direct_contact_by_recruiters_is_okay = models.BooleanField()
    internship = models.BooleanField()
    non_profit_organization = models.BooleanField()
    telecommuting_okay = models.BooleanField()
    compensation = models.CharField(max_length=200)


class GaragePost(Post):
    start_day = models.CharField(max_length=50)
    duration = models.IntegerField()


class SaleGarage(Post):
    sale_date1 = models.CharField(max_length=50)
    sale_date2 = models.CharField(max_length=50)
    sale_date3 = models.CharField(max_length=50)
    start_time = models.CharField(max_length=50)
    include_ads = models.BooleanField()


class CarPost(Post):
    model_year = models.IntegerField()
    make_model = models.CharField(max_length=100)
    odometer = models.IntegerField()
    condition = models.CharField(max_length=50)
    cylinder = models.IntegerField()
    drive = models.CharField(max_length=50)
    fuel = models.CharField(max_length=50)
    transmission = models.CharField(max_length=50)
    paint_color = models.CharField(max_length=50)
    size = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    title_status = models.CharField(max_length=50, blank=True, null=True)
    vin = models.CharField(max_length=50, blank=True, null=True)
    cryptocurrency_ok = models.BooleanField()
    include_ads = models.BooleanField()


class MotorCyclePost(Post):
    model_year = models.IntegerField()
    make_model = models.CharField(max_length=100)
    odometer = models.IntegerField()
    engine_displacement = models.IntegerField()
    condition = models.CharField(max_length=50)
    fuel = models.CharField(max_length=50)
    transmission = models.CharField(max_length=50)
    paint_color = models.CharField(max_length=50)
    title_status = models.CharField(max_length=50, blank=True, null=True)
    vin = models.CharField(max_length=50, blank=True, null=True)
    cryptocurrency_ok = models.BooleanField()
    include_ads = models.BooleanField()


class BoatPost(Post):
    engine_hours = models.IntegerField()
    length_overall = models.IntegerField()
    make = models.CharField(max_length=100, null=True, blank=True)
    model = models.CharField(max_length=100, null=True, blank=True)
    made_year = models.IntegerField()
    condition = models.CharField(max_length=50)
    propulsion_type = models.CharField(max_length=50)
    cryptocurrency_ok = models.BooleanField()
    include_ads = models.BooleanField()


class TrailerPost(Post):
    make = models.CharField(max_length=100, null=True, blank=True)
    model = models.CharField(max_length=100, null=True, blank=True)
    made_year = models.IntegerField()
    condition = models.CharField(max_length=50)
    paint_color = models.CharField(max_length=50)
    size = models.CharField(max_length=50)    
    cryptocurrency_ok = models.BooleanField()
    include_ads = models.BooleanField()


class AptPost(Post):
    area = models.FloatField()
    available_on = models.DateField()    
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    type = models.CharField(max_length=50)
    laundry = models.CharField(max_length=50, blank=True, null=True)
    parking = models.CharField(max_length=50, blank=True, null=True)
    cats_ok = models.BooleanField(default=False)
    dogs_ok = models.BooleanField(default=False)
    furnished = models.BooleanField(default=False)
    no_smoking = models.BooleanField(default=False)
    wheelchair = models.BooleanField(default=False)


class SubletPost(Post):
    area = models.FloatField()
    available_on = models.DateField()    
    private_bed = models.CharField(max_length=50, blank=True, null=True)
    private_bath = models.CharField(max_length=50, blank=True, null=True)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    type = models.CharField(max_length=50)
    laundry = models.CharField(max_length=50, blank=True, null=True)
    parking = models.CharField(max_length=50, blank=True, null=True)
    cats_ok = models.BooleanField(default=False)
    dogs_ok = models.BooleanField(default=False)
    furnished = models.BooleanField(default=False)
    no_smoking = models.BooleanField(default=False)
    wheelchair = models.BooleanField(default=False)


class AntiquePost(Post):
    make = models.CharField(max_length=100, null=True, blank=True)
    model = models.CharField(max_length=100, null=True, blank=True)
    size = models.CharField(max_length=100, null=True, blank=True)
    condition = models.CharField(max_length=100, null=True, blank=True)
    cryptocurrency_ok = models.BooleanField()
    include_ads = models.BooleanField()


class CellPhonePost(AntiquePost):
    mobile_os = models.CharField(max_length=100, null=True, blank=True)


class BookPost(Post):
    size = models.CharField(max_length=100, null=True, blank=True)
    condition = models.CharField(max_length=100, null=True, blank=True)
    cryptocurrency_ok = models.BooleanField()
    include_ads = models.BooleanField()


class CDPost(Post):
    media_type = models.CharField(max_length=100, null=True, blank=True)
    condition = models.CharField(max_length=100, null=True, blank=True)
    cryptocurrency_ok = models.BooleanField()
    include_ads = models.BooleanField()


class TicketPost(Post):
    event_date = models.DateField()
    num_avail = models.IntegerField()
    venue = models.CharField(max_length=100, null=True, blank=True)
    cryptocurrency_ok = models.BooleanField()
    include_ads = models.BooleanField()


class AutoWheelPost(Post):
    cryptocurrency_ok = models.BooleanField()
    include_ads = models.BooleanField()


class RealEstatePost(Post):
    area = models.FloatField()
    available_on = models.DateField()    
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    type = models.CharField(max_length=50)
    laundry = models.CharField(max_length=50, blank=True, null=True)
    parking = models.CharField(max_length=50, blank=True, null=True)
    furnished = models.BooleanField(default=False)
    no_smoking = models.BooleanField(default=False)
    wheelchair = models.BooleanField(default=False)
    licensed = models.BooleanField(default=True)


class RoomPost(Post):
    area = models.FloatField()
    available_on = models.DateField()    
    private_bed = models.CharField(max_length=50, blank=True, null=True)
    private_bath = models.CharField(max_length=50, blank=True, null=True)
    laundry = models.CharField(max_length=50, blank=True, null=True)
    parking = models.CharField(max_length=50, blank=True, null=True)
    cats_ok = models.BooleanField(default=False)
    dogs_ok = models.BooleanField(default=False)
    furnished = models.BooleanField(default=False)
    no_smoking = models.BooleanField(default=False)
    wheelchair = models.BooleanField(default=False)


class OfficePost(Post):
    area = models.FloatField()


class BuyGigPost(Post):
    direct_contact_by_recruiters_is_okay = models.BooleanField()
    compensation = models.CharField(max_length=200)
    pay = models.BooleanField()


class LicensePost(Post):
    licensed = models.BooleanField()
    description = models.CharField(max_length=200)
