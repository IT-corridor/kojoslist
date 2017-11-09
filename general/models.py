# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="info")
    forum_handle = models.CharField(max_length=100, blank=True, null=True)
    default_site = models.CharField(max_length=100, blank=True, null=True)
    duration = models.CharField(max_length=100, blank=True, null=True)

    def __unicode__(self):
        return self.user.username


class Category(models.Model):
    parent = models.ForeignKey("Category", blank=True, null=True)
    name = models.CharField(max_length=50)
    columns = models.IntegerField(default=1)
    column = models.IntegerField(default=1)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Post(models.Model):
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField()
    status = models.CharField(max_length=50, blank=True, null=True)
    category = models.ForeignKey(Category)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField()
    owner = models.ForeignKey(User)
    region = models.CharField(max_length=50, blank=True, null=True)
    language = models.CharField(max_length=50, default='english')
    # contact
    mail_relay = models.BooleanField()
    real_email = models.BooleanField()
    no_reply = models.BooleanField()
    by_phone = models.BooleanField()
    by_text = models.BooleanField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    extension = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    allow_other_contact = models.BooleanField()

    def __unicode__(self):
        return self.title


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
    start_day = models.DateField()
    duration = models.IntegerField()


class SaleGarage(Post):
    sale_date1 = models.DateField()
    sale_date2 = models.DateField()
    sale_date3 = models.DateField()
    start_time = models.TimeField()
    include_ads = models.BooleanField()


class Search(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    alert = models.BooleanField()
    hits = models.IntegerField()

    def __unicode__(self):
        return self.name


class Image(models.Model):
    post = models.ForeignKey(Post)
    img = models.ImageField()

    def __unicode__(self):
        return self.post.title


class Detail(models.Model):
    def __unicode__(self):
        return self.name


class Favourite(models.Model):
    owner =  models.ForeignKey(User)
    post = models.ForeignKey(Post)

    def __unicode__(self):
        return '{} - {}'.format(self.owner.first_name, self.post.title)


class Hidden(models.Model):
    owner =  models.ForeignKey(User)
    post = models.ForeignKey(Post, related_name='post')

    def __unicode__(self):
        return '{} - {}'.format(self.owner.first_name, self.post.title)


class Country(models.Model):
    shortname = models.CharField(max_length=3)
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=150)
    country = models.ForeignKey(Country)

    def __unicode__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=30)
    state = models.ForeignKey(State)

    def __unicode__(self):
        return self.name

