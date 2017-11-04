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
    parent = models.ForeignKey("Category")
    name = models.CharField(max_length=50)
    columns = models.IntegerField()
    
    def __unicode__(self):
        return self.name


class Contact(models.Model):
    mail_realy = models.BooleanField()
    real_email = models.BooleanField()
    no_reply = models.BooleanField()
    by_phone = models.BooleanField()
    by_text = models.BooleanField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    extension = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)

    def __unicode__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField()
    status = models.CharField(max_length=50, blank=True, null=True)
    category = models.ForeignKey(Category)
    # detail = models.ForeignKey(Detail)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField()
    owner = models.ForeignKey(User)
    contact = models.ForeignKey(Contact, blank=True, null=True)
    allow_other_contact = models.BooleanField()

    def __unicode__(self):
        return self.title


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
