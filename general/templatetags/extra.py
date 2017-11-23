from django import template
import datetime

register = template.Library()

@register.filter
def raised_percent(campaign, css=False):
    percent = campaign.raised * 100 / campaign.budget
    if css and percent > 100:
        percent = 100
    return percent

@register.filter
def ramained_days(campaign):
    return (campaign.created_at + datetime.timedelta(days=campaign.duration) - datetime.datetime.now().date()).days
    

