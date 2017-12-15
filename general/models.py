# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser

VSTATUS = (
    ('unverified', 'Unverified'),
    ('awaiting_approve', 'Awaiting Approve'),
    ('approved', 'Approved')
)

class Customer(AbstractUser):
    avatar = models.CharField(max_length=100, default="default_avatar.png")
    phone = models.CharField(max_length=20, blank=True, null=True)
    phone_verified = models.BooleanField(default=False)
    dob = models.CharField(max_length=50, blank=True, null=True)
    forum_handle = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    # cache location
    default_site = models.CharField(max_length=100, blank=True, null=True)
    duration = models.CharField(max_length=100, blank=True, null=True)
    v_statue = models.CharField(max_length=50, choices=VSTATUS, default='unverified')
    id_photo = models.ImageField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username


class Category(models.Model):
    parent = models.ForeignKey("Category", blank=True, null=True)
    name = models.CharField(max_length=50)
    columns = models.IntegerField(default=1)
    column = models.IntegerField(default=1)
    form = models.CharField(max_length=50, default='Post')
    price = models.FloatField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ads Category'
        verbose_name_plural = 'Ads Categories'


class Country(models.Model):
    sortname = models.CharField(max_length=3)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Countries'


class State(models.Model):
    name = models.CharField(max_length=150)
    country = models.ForeignKey(Country)

    def __str__(self):
        return self.name.encode('utf-8')


class City(models.Model):
    """
    cities do not have district
    districts have district as parent city
    """
    name = models.CharField(max_length=30)
    state = models.ForeignKey(State)
    district = models.ForeignKey("City", blank=True, null=True, related_name='districts')

    def __str__(self):
        return self.name.encode('utf-8')

    class Meta:
        verbose_name_plural = 'Cities'


class Post(models.Model):
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField()
    status = models.CharField(max_length=50, blank=True, null=True)
    category = models.ForeignKey(Category)
    price = models.FloatField(default=0, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(Customer)
    region = models.ForeignKey(City, blank=True, null=True)
    language = models.CharField(max_length=50, blank=True, null=True)
    # contact
    mail_relay = models.BooleanField(default=False)
    real_email = models.BooleanField(default=False)
    no_reply = models.BooleanField(default=False)
    by_phone = models.BooleanField(default=False)
    by_text = models.BooleanField(default=False)
    phone = models.CharField(max_length=20, blank=True, null=True)
    extension = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    allow_other_contact = models.BooleanField(default=False)

    def __str__(self):
        return self.title


PURCHASE_TYPE = (
    ('direct', 'DIRECT'),
    ('escrow', 'ESCROW')
)

PURCHASE_STATUS = (
    (0, 'FINISHED SUCCESSFULLY'),
    (1, 'WAIT RELEASE'),
    (2, 'UNDER DISPUTE')
)

class PostPurchase(models.Model):
    post = models.ForeignKey(Post)
    purchaser = models.ForeignKey(Customer)
    type = models.CharField(max_length=20, choices=PURCHASE_TYPE)
    contact = models.TextField(blank=True, null=True)
    transaction = models.CharField(max_length=100)
    status = models.IntegerField(choices=PURCHASE_STATUS, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} - {}'.format(self.post.title, self.purchaser.username)


class Review(models.Model):
    """
    review on post
    """
    post = models.ForeignKey(Post)
    rater = models.ForeignKey(Customer)
    rating = models.FloatField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} - {}'.format(self.post.title, self.rater.username)


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
    title_status = models.CharField(max_length=50)


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


class RoomPost(Post):
    area = models.FloatField()
    available_on = models.DateField()    
    private_bed = models.CharField(max_length=50)
    private_bath = models.CharField(max_length=50)
    laundry = models.CharField(max_length=50, blank=True, null=True)
    parking = models.CharField(max_length=50, blank=True, null=True)
    cats_ok = models.BooleanField(default=False)
    dogs_ok = models.BooleanField(default=False)
    furnished = models.BooleanField(default=False)
    no_smoking = models.BooleanField(default=False)
    wheelchair = models.BooleanField(default=False)


class BuyGigPost(Post):
    direct_contact_by_recruiters_is_okay = models.BooleanField()
    compensation = models.CharField(max_length=200)
    pay = models.BooleanField()


class LicensePost(Post):
    licensed = models.BooleanField()
    description = models.CharField(max_length=200)


class Search(models.Model):
    keyword = models.CharField(max_length=100)
    category = models.ForeignKey(Category, blank=True, null=True)
    city = models.ForeignKey(City, blank=True, null=True)
    state = models.ForeignKey(State, blank=True, null=True)
    owner = models.ForeignKey(Customer)
    created_at = models.DateTimeField(auto_now_add=True)
    alert = models.BooleanField(default=True)
    search_title = models.BooleanField(default=False)
    has_image = models.BooleanField(default=False)
    posted_today = models.BooleanField(default=False)
    min_price = models.FloatField(blank=True, null=True)
    max_price = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.owner.username

    class Meta:
        verbose_name = 'Subscribe'
        verbose_name_plural = 'Subscribes'


class Image(models.Model):
    post = models.ForeignKey(Post, related_name='images')
    name = models.CharField(max_length=100)

    def __str__(self):
        return '{} - {}'.format(self.post.title, self.name)



class Favourite(models.Model):
    owner =  models.ForeignKey(Customer, related_name="favourites")
    post = models.ForeignKey(Post)

    def __str__(self):
        return '{} - {}'.format(self.owner.first_name, self.post.title)


class Hidden(models.Model):
    owner =  models.ForeignKey(Customer)
    post = models.ForeignKey(Post, related_name='post')

    def __str__(self):
        return '{} - {}'.format(self.owner.first_name, self.post.title)


class Perk(models.Model):
    title = models.CharField(max_length=200)
    campaign = models.ForeignKey("Campaign")
    price = models.IntegerField()
    retail = models.IntegerField(default=0)
    description = models.TextField()
    num_avail = models.IntegerField(default=1000000)
    num_claimed = models.IntegerField(default=0)
    image = models.ImageField(upload_to="perks", blank=True, null=True)

    def __str__(self):
        return '{} - {}'.format(self.campaign.title, self.title)


class PerkClaim(models.Model):
    campaign = models.ForeignKey("Campaign", related_name="claims")
    # null for donate
    perk = models.ForeignKey(Perk, blank=True, null=True, related_name="claims")
    contact = models.TextField(blank=True, null=True)
    # null for Anonymous
    claimer = models.ForeignKey(Customer, blank=True, null=True)
    amount = models.IntegerField()      # in cent
    transaction = models.CharField(max_length=100)

    def __str__(self):
        return self.campaign.title


class CampCategory(models.Model):
    parent = models.ForeignKey("CampCategory", blank=True, null=True)
    name = models.CharField(max_length=50)
    column = models.IntegerField(default=1)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Campaign Category'
        verbose_name_plural = 'Campaign Categories'


STAGES = [
    ('concept', 'CONCEPT'),
    ('prototype', 'PROTOTYPE'),
    ('production', 'PRODUCTION'),
    ('shipping', 'SHIPPING')
]

class Campaign(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(CampCategory)
    budget = models.IntegerField()
    raised = models.IntegerField(default=0)
    over_image = models.ImageField(upload_to="campaigns")
    overview = models.TextField()
    content = models.TextField()
    stage = models.CharField(max_length=200, choices=STAGES)
    duration = models.IntegerField()
    tagline = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    # youtube video keys
    videos = models.TextField(blank=True, null=True)
    owner =  models.ForeignKey(Customer)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
