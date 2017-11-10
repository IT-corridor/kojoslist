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

from general.models import *
from general.forms import *


def home(request):
    rndr_str = globoard_display_world_countries()
    return render(request, 'index.html', {'rndr_str': rndr_str})

def my_ads(request):
    return render(request, 'my_ads.html')

def post_ads(request):
    mcategories = Category.objects.filter(parent__isnull=True)
    countries = Country.objects.all()
    return render(request, 'post_ads.html', {
        'mcategories': mcategories,
        'countries': countries
    })

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
    return render(request, 'rndr_category.html', {'categories': result})

def add_post(request):
    cc = request.GET.get('cc')
    if request.method == 'GET':
        if not cc:
            categories = POST_DETAIL_CATEGORY.keys()
            request.session['category'] = []
        else:
            categories = POST_DETAIL_CATEGORY
            for tc in request.session['category']:
                categories = categories[tc]            

            request.session['category'].append(cc)
            request.session.modified = True
            if not cc in categories:
                return HttpResponse('404 No such category!'+str(request.session['category']), status=404)
            categories = categories[cc]

            if not isinstance(categories, dict):
                category = categories[0]
                template = 'post/' + categories[1]
                request.session['form'] = categories[2]
                request.session.modified = True

                return render(request, template, {
                    'category': category,
                })

        return render(request, 'add_post.html', {
            'categories': categories,
            'head': cc
        })
    else:
        # a specific parameter
        form = request.session['form']
        if form.is_valid():
            form.save()
        return HttpRedirect(request, 'success.html')

def posts(request):
    return render(request, 'posts.html', {})
    # return render(request, 'post/jobpost.html', {})
    return render(request, 'post/salegarage.html', {})

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
    return render(request, template)
