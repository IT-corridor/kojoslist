# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import json

from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.template.loader import render_to_string
from django.db.models import Q

from general.models import *
from general.forms import *

get_class = lambda x: globals()[x]


def home(request):
    rndr_str = globoard_display_world_countries()
    return render(request, 'index.html', {'rndr_str': rndr_str})

def my_ads(request):
    posts = Post.objects.filter(owner=request.user)
    posts = get_posts_with_image(posts)
    return render(request, 'my_ads.html', {'posts': posts})

@csrf_exempt
def search_ads(request):
    keyword = request.POST.get('keyword')
    posts = Post.objects.filter(owner=request.user).filter(Q(title__icontains=keyword) | Q(content__icontains=keyword))
    posts = get_posts_with_image(posts)
    rndr_str = render_to_string('_post_list.html', {'posts': posts})
    return HttpResponse(rndr_str)

def get_posts_with_image(posts):
    posts_with_image = []
    for post in posts:
        image = Image.objects.filter(post=post).first()
        img_name = image.name if image else 'dummy.jpg'
        posts_with_image.append((post, img_name))
    return posts_with_image

def profile(request):
    state_id = request.GET.get('state_id')
    mycusid = request.GET.get('mycusid')

    if state_id:
        rndr_str = display_regions_of_state(state_id)
    elif mycusid:
        rndr_str = display_regions_of_state(mycusid) + globoard_display_world_countries('hidden')
    else:
        rndr_str = globoard_display_world_countries()

    return render(request, 'profile.html', {'rndr_str': rndr_str})

def display_regions_of_state(sortname):
    states = State.objects.filter(country__sortname=sortname.upper())
    rndr_str = ''
    for state in states:
        rndr_str += "<li class='regions_li' data-type='regions' data-pid='{0}' ><a href='#'>{0}</a></li>".format(state.name)

    if states:
        rndr_str = "<ul class='list'>" + rndr_str + "</ul>"
    return rndr_str

def globoard_display_world_countries(css_class=''):
    rndr_str = "<ul class='country-list {}'>".format(css_class)
    for country in Country.objects.all():
        rndr_str += '<li><a href="/profile?state_id={0}#countries/{0}/{0}-all" class="show_country" data-country="{1}">{2}</a></li>'.format(country.sortname.lower(), country.sortname, country.name)
    return rndr_str + '</ul>'

def ajax_region(request):
    """
    get sub region like states or cities
    """
    state_id = request.GET.get('state_id')
    sec_name = request.GET.get('sec_name')

    country = Country.objects.filter(sortname=state_id.upper()).first()
    result = []
    if country:
        states = State.objects.filter(country=country)
        num_states = states.count()        
        result = [{'no': num_states, 'id': state.id, 'name': state.name, 'type': 'regions', 'country_id': state.country_id} 
                  for state in states]
        if not result:
            result = [{'msg': 'not found', 'type': 'regions', 'no': 0}]
    else:
        if sec_name:
            state_id = sec_name.split(',')[0]
        cities = City.objects.filter(state__name=state_id)
        num_cities = cities.count()        
        result = [{'no': num_cities, 'id': city.id, 'name': city.name, 'type': 'cities', 'state_id': city.state_id} 
                  for city in cities]
        if not result:
            result = [{'msg': 'not found', 'type': 'cities', 'no': 0}]

    return JsonResponse(result, safe=False)

def get_category_by_location_id(request):
    city = request.GET.get('city')  # not used

    result = []
    for column in range(1, 7):
        _result = []
        for mc in Category.objects.filter(parent__isnull=True, column=column):
            cc = Category.objects.filter(parent=mc)
            _result += [(mc, cc)]
        result += [_result]
    return render(request, '_category.html', {'categories': result})

def post_ads(request, ads_id):
    if request.method == 'GET':
        mcategories = Category.objects.filter(parent__isnull=True)
        countries = Country.objects.all()
        
        if ads_id:
            post = Post.objects.get(id=ads_id)
            model = eval(post.category.form)
            post = model.objects.get(id=ads_id)
            states = State.objects.filter(country=post.region.state.country)
            cities = City.objects.filter(state=post.region.state)
            images = Image.objects.filter(post=post)
            detail_template = 'post/{}.html'.format(post.category.form)
        else:
            post = None
            states = None
            cities = None
            images = None
            detail_template = 'post/Post.html'

        return render(request, 'post_ads.html', {
            'mcategories': mcategories,
            'countries': countries,
            'states': states,
            'cities': cities,
            'images': images,
            'post': post,
            'detail_template': detail_template
        })
    else:
        form_name = request.POST.get('ads_form') + 'Form'
        form = get_class(form_name)

        if ads_id:
            model = eval(request.POST.get('ads_form'))
            instance = model.objects.get(id=ads_id)
            form = form(request.POST, instance=instance)
        else:
            form = form(request.POST)
        images = request.POST.getlist('uploded_id[]')
        
        if form.is_valid():
            post = form.save()
            for img in images:
                if img:
                    Image.objects.create(post=post, name=img)
            # for img in images if img:
            #     os.remove(settings.BASE_DIR+'/static/media/'+image_name)

        print form.errors, '$$$$$$$$'
        return HttpResponseRedirect(reverse('my-ads'))

@csrf_exempt
def auth_process(request):
    unique_id = request.POST.get('unique_id')
    action = request.POST.get('action')

    if action == 'userpro_process_form':
        username = request.POST.get('username_or_email-'+unique_id)
        passwd = request.POST.get('user_pass-'+unique_id)

        user = authenticate(username=username, password=passwd)
        if user:
            res = {"error":"","redirect_uri":"/profile/"}
            login(request, user)
        else:
            res = {"error":{"user_pass":"The password you entered is incorrect"}}

        return JsonResponse(res, safe=False)

def ulogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def get_sub_info(request):
    """
    ajax call for sub category, state, city
    """
    obj_id = request.GET.get('obj_id')
    sc_type = request.GET.get('type') # Category, State, City
    rndr_str = '<option value="">-Select-</option>'

    if sc_type == 'category':
        objects = Category.objects.filter(parent__id=obj_id)
    elif sc_type == 'state':
        objects = State.objects.filter(country__id=obj_id)
    else:
        objects = City.objects.filter(state__id=obj_id)
        
    for sc in objects:
        rndr_str += '<option value="{}">{}</option>'.format(sc.id, sc.name)
    return HttpResponse(rndr_str)

@csrf_exempt
def upload_image(request):
    myfile = request.FILES['images']
    fs = FileSystemStorage()
    filename = fs.save('static/media/'+myfile.name, myfile)
    uploaded_file_url = fs.url(filename)
    res = {"image_url": "/"+uploaded_file_url,"image_name": uploaded_file_url[13:]}
    return JsonResponse(res, safe=False)

@csrf_exempt
def delete_image(request):
    image_name = request.POST.get('image_name')
    os.remove(settings.BASE_DIR+'/static/media/'+image_name)
    return HttpResponse('')

def get_post_detail(request):
    obj_id = request.GET.get('obj_id')
    form_name = Category.objects.get(id=obj_id).form
    template = 'post/{}.html'.format(form_name)
    html = render_to_string(template)

    return JsonResponse({'html': html, 'form': form_name}, safe=False)

@csrf_exempt
def active_deactive_ads(request):
    ads = request.POST.get('ads_id')
    status = request.POST.get('status')
    Post.objects.filter(id=ads).update(status=status)
    return HttpResponse('ok')

@csrf_exempt
def delete_ads(request):
    ads = request.POST.get('ads_id')
    Post.objects.filter(id=ads).delete()
    return HttpResponse('ok')


