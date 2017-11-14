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
from django.conf.urls import url
from django.contrib import admin

from general.views import *

admin.site.site_header = "Globalboard Admin"

urlpatterns = [
    url(r'^admin/', admin.site.urls),
]


urlpatterns += [
    url(r"^$", home, name="home"),
    url(r"^delete_ads$", delete_ads, name="delete_ads"),
    url(r"^breadcrumb$", breadcrumb, name="breadcrumb"),
    url(r"^search_ads$", search_ads, name="search_ads"),
    url(r"^active_deactive_ads", active_deactive_ads, name="active_deactive_ads"),
    url(r"^get_post_detail$", get_post_detail, name="get_post_detail"),
    url(r"^profile", profile, name="profile"),
    url(r"^toggle_favourite", toggle_favourite, name="toggle_favourite"),
    url(r"^my-ads", my_ads, name="my-ads"),
    url(r"^my-favourites", my_favourites, name="my-favourites"),
    url(r"^post-ads/(?P<ads_id>\d*)", post_ads, name="post-ads"),
    url(r"^ads/(?P<ads_id>\d*)", view_ads, name="view-ads"),
    url(r"^category-ads/(?P<category_id>\d*)", category_ads, name="category-ads"),
    url(r"^upload-image$", upload_image, name="upload-image"),
    url(r"^delete-image$", delete_image, name="delete-image"),
    url(r"^get_sub_info$", get_sub_info, name="get_sub_info"),
    url(r"^logout$", ulogout, name="logout"),
    url(r"^region-ads/(?P<region_id>\d*)", region_ads, name="region-ads"),
    url(r"^get_regions", get_regions, name="get_regions"),
    url(r"^auth_process", auth_process, name="auth_process"),   
    url(r"^send_friend_email", send_friend_email, name="send_friend_email"), 
    url(r"^send_reply_email", send_reply_email, name="send_reply_email"),        
    url(r"^search_ads_all", search_ads_all, name="search_ads_all"),        
    url(r"^get_category_by_location_id", get_category_by_location_id, name="get_category_by_location_id"),    
]