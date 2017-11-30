# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.db.models.signals import post_save
from django.conf import settings

from general.models import *
from general.utils import send_email

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
        for ss in Search.objects.all().exclude(owner=instance.owner):
            if not ss.keyword or ss.keyword.lower() in instance.title.lower() or ss.keyword.lower() in instance.content.lower():
                if ss.city == instance.region or ss.state == instance.region.state:
                    if ss.category == instance.category or ss.category == instance.category.parent:
                        subscription_info = ''

                        content = """
                            1 new result for your subscription ( {} ) as of {}<br><br>
                            <a href="http://18.216.225.192/ads/{}">{}</a><br><br>
                            <a href="http://18.216.225.192/my-subscribe">Review all saved searches.</a><br><br>
                            Thank you for using <a href="http://18.216.225.192/">Globalboard</a>.                         
                        """.format(ss.category.name, str(instance.created_at), instance.id, instance.title)
                        send_email(settings.FROM_EMAIL, 'Globalboard Subscription Alarm', ss.owner.email, content)
    except Exception, e:
        print e, '@@@@@@@@@'