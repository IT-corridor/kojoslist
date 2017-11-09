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

admin.site.site_header = "Kojo's List Admin"

urlpatterns = [
    url(r'^admin/', admin.site.urls),
]


urlpatterns += [
    url(r"^$", home, name="home"),
    url(r"^login$", login, name="login"),
    url(r"^account$", account, name="account"),
    url(r"^add_post", add_post, name="add_post"),
    url(r"^profile", profile, name="profile"),
    url(r"^posts$", posts, name="posts"),
    url(r"^ajax_region", ajax_region, name="ajax_region"),    
    url(r"^get_category_by_location_id", get_category_by_location_id, name="get_category_by_location_id"),    
]