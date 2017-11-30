"""kojoslist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from general.views import *

admin.site.site_header = "Globalboard Admin"

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
]


urlpatterns += [
    url(r"^$", home, name="home"),
    url(r"^delete_ads$", delete_ads, name="delete_ads"),
    url(r"^breadcrumb$", breadcrumb, name="breadcrumb"),
    url(r"^search_ads$", search_ads, name="search_ads"),
    url(r"^rate_ads$", rate_ads, name="rate_ads"),
    url(r"^search_camps$", search_camps, name="search_camps"),    
    url(r"^active_deactive_ads", active_deactive_ads, name="active_deactive_ads"),
    url(r"^get_post_detail$", get_post_detail, name="get_post_detail"),
    url(r"^profile", profile, name="profile"),
    url(r"^toggle_favourite", toggle_favourite, name="toggle_favourite"),
    url(r"^my-ads", my_ads, name="my-ads"),
    url(r"^explorer-campaigns", explorer_campaigns, name="explorer-campaigns"),
    url(r"^my-campaigns", my_campaigns, name="my-campaigns"),
    url(r"^my-favourites", my_favourites, name="my-favourites"),
    url(r"^my-subscribe", my_subscribe, name="my-subscribe"),
    url(r"^post-ads/(?P<ads_id>\d*)", post_ads, name="post-ads"),
    url(r"^post-camp/(?P<camp_id>\d*)", post_camp, name="post-camp"),
    url(r"^ads/(?P<ads_id>\d*)", view_ads, name="view-ads"),
    url(r"^campaigns/(?P<camp_id>\d*)", view_campaign, name="view-campaign"),
    url(r"^category-ads/(?P<category_id>\d*)", category_ads, name="category-ads"),
    url(r"^upload-image$", upload_image, name="upload-image"),
    url(r"^delete-image$", delete_image, name="delete-image"),
    url(r"^get_sub_info$", get_sub_info, name="get_sub_info"),
    url(r"^logout$", ulogout, name="logout"),
    url(r"^region-ads/st/(?P<region_id>\d+)", region_ads, {'region': 'state'}, name="state-ads"),
    url(r"^region-ads/ct/(?P<region_id>\d+)", region_ads, {'region': 'city'}, name="city-ads"),
    url(r"^region-ads/wd/(?P<region_id>\d*)", region_ads, {'region': 'world'}, name="world-ads"),
    url(r"^get_regions", get_regions, name="get_regions"),
    url(r"^verify_phone", verify_phone, name="verify_phone"),   
    url(r"^confirm-phone", confirm_phone, name="confirm-phone"),   
    url(r"^send_vcode", send_vcode, name="send_vcode"),   
    url(r"^upload_id", upload_id, name="upload_id"),   
    url(r"^my-account", my_account, name="my-account"),   
    url(r"^send_friend_email", send_friend_email, name="send_friend_email"), 
    url(r"^send_reply_email", send_reply_email, name="send_reply_email"),        
    url(r"^create-subscribe", create_subscribe, name="create-subscribe"),        
    url(r"^remove-subscribe", remove_subscribe, name="remove-subscribe"),        
]