# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from django.db import models
from django.db.models.signals import pre_delete
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import AbstractUser

from general.utils import send_email


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
    v_statue = models.CharField(max_length=50)
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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


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
        return self.name


class City(models.Model):
    name = models.CharField(max_length=30)
    state = models.ForeignKey(State)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Cities'


class Post(models.Model):
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField()
    status = models.CharField(max_length=50, blank=True, null=True)
    category = models.ForeignKey(Category)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(Customer)
    region = models.ForeignKey(City)
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


class Search(models.Model):
    keyword = models.CharField(max_length=100)
    category = models.ForeignKey(Category, blank=True, null=True)
    city = models.ForeignKey(City, blank=True, null=True)
    state = models.ForeignKey(State, blank=True, null=True)
    owner = models.ForeignKey(Customer)
    created_at = models.DateTimeField(auto_now_add=True)

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


@receiver(pre_delete, sender=Image, dispatch_uid='image_delete_signal')
def delete_image_file(sender, instance, using, **kwargs):
    try:
        os.remove(settings.BASE_DIR+'/static/media/'+instance.name)
    except Exception:
        pass

@receiver(post_save, sender=Post)
@receiver(post_save, sender=JobPost)
@receiver(post_save, sender=GaragePost)
@receiver(post_save, sender=SaleGarage)
def apply_subscribe(sender, instance, **kwargs):    
    try:
        for ss in Search.objects.all().exclue(owner=instance.owner):
            if not ss.keyword or ss.keyword.lower() in instance.title.lower() or ss.keyword.lower() in instance.content.lower():
                if ss.city == instance.region or ss.state == instance.region.state:
                    if ss.category == instance.category or ss.category == instance.category.parent:
                        content = """
                            1 new result for all posts as of {}<br><br>
                            <a href="/ads/{}">{}</a><br><br>
                            <a href="/my-subscribe">Review all saved searches.</a><br><br>
                            Thank you for using <a href="/">Globalboard</a>.                         
                        """.format(str(instance.created_at), instance.id, instance.title)
                        send_email(settings.FROM_EMAIL, 'Globalboard Subscripttion', ss.owner.email, content)
    except Exception:
        pass

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

