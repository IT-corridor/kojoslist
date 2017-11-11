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
    url(r"^search_ads$", search_ads, name="search_ads"),
    url(r"^active_deactive_ads", active_deactive_ads, name="active_deactive_ads"),
    url(r"^get_post_detail$", get_post_detail, name="get_post_detail"),
    url(r"^profile", profile, name="profile"),
    url(r"^get_ads", get_ads, name="get_ads"),
    url(r"^my-ads", my_ads, name="my-ads"),
    url(r"^post-ads/(?P<ads_id>\d*)", post_ads, name="post-ads"),
    url(r"^ads/(?P<ads_id>\d*)", view_ads, name="view-ads"),
    url(r"^upload-image$", upload_image, name="upload-image"),
    url(r"^delete-image$", delete_image, name="delete-image"),
    url(r"^get_sub_info$", get_sub_info, name="get_sub_info"),
    url(r"^logout$", ulogout, name="logout"),
    url(r"^ajax_region", ajax_region, name="ajax_region"),
    url(r"^auth_process", auth_process, name="auth_process"),    
    url(r"^get_category_by_location_id", get_category_by_location_id, name="get_category_by_location_id"),    
]