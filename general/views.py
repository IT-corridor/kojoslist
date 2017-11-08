# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

from general.models import *
from general.forms import *


POST_DETAIL_CATEGORY = {
    "job offered": {
        "accounting/finance": PostForm,
        "admin/office": ['admin/office', 'jobpost.html', 'JobPostForm'],
        "architect/engineer/cad (no IT/computer jobs here please )": PostForm,
        "art/media/design": PostForm,
        "business/mgmt": PostForm,
        "customer service": PostForm,
        "education/teaching": PostForm,
        "et cetera": PostForm,
        "food/beverage/hospitality": PostForm,
        "general labor": PostForm,
        "government": PostForm,
        "healthcare": PostForm,
        "human resource": PostForm,
        "internet engineering": PostForm,
        "legal/paralegal": PostForm,
        "manufacturing": PostForm,
        "marketing/advertising/pr": PostForm,
        "nonprofit": PostForm,
        "real estate": PostForm,
        "retail/wholesale": PostForm,
        "sales": PostForm,
        "salon/spa/fitness": PostForm,
        "science/biotech": PostForm,
        "security": PostForm,
        "skilled trades/artisan": PostForm,
        "software/qa/dba/etc": PostForm,
        "systems/networking": PostForm,
        "technical support": PostForm,
        "transportation": PostForm,
        "tv/film/video/radio": PostForm,
        "web/html/info design": PostForm,
        "writing/editing": PostForm
    },
    "gig offered (I'm hiring for a short-term, small or odd job)": {
        "I want to hire someone": PostForm,
        "I have a service to offer ": PostForm
    },
    "resume / job wanted": {
        "I'm an individual seeking employment": PostForm,
        "I'm offering or advertising a service": PostForm,
        "I'm offering a job": PostForm,
        "I'm offering childcare": PostForm
    },
    "housing offered": {
        "rooms & shares": PostForm,
        "apts/housing for rent (no shares, roommates, or sublets please! )": PostForm,
        "housing swap": PostForm,
        "office & commercial": PostForm,
        "parking & storage": PostForm,
        "real estate - by broker": PostForm,
        "real estate - by owner": PostForm,
        "sublets & temporary": PostForm,
        "vacation rentals": PostForm
    },
    "housing wanted": {
        "apts wanted": PostForm,
        "real estate wanted": PostForm,
        "room/share wanted": PostForm,
        "sublet/temp wanted": PostForm
    },
    "for sale by owner": {
        "antiques - by owner": PostForm,
        "appliances - by owner": PostForm,
        "arts & crafts - by owner": PostForm,
        "atvs, utvs, snowmobiles - by owner": PostForm,
        "auto parts - by owner": PostForm,
        "auto wheels & tires - by owner": PostForm,
        "baby & kid stuff - by owner (no illegal sales of recall items, e.g. drop-side cribs, recalled strollers )": PostForm,
        "barter": PostForm,
        "bicycle parts - by owner": PostForm,
        "bicycles - by owner": PostForm,
        "boat parts - by owner": PostForm,
        "boats - by owner": PostForm,
        "books & magazines - by owner": PostForm,
        "business/commercial - by owner": PostForm,
        "cars & trucks - by owner": PostForm,
        "cds / dvds / vhs - by owner (no pornography please )": PostForm,
        "cell phones - by owner": PostForm,
        "clothing & accessories - by owner": PostForm,
        "collectibles - by owner": PostForm,
        "computer parts - by owner": PostForm,
        "computers - by owner": PostForm,
        "electronics - by owner": PostForm,
        "farm & garden - by owner (legal sales of agricultural livestock OK )": PostForm,
        "free stuff (no \"wanted\" ads, pets, promotional giveaways, or intangible/digital items please )": PostForm,
        "furniture - by owner": PostForm,
        "garage & moving sales (no online or virtual sales here please )": PostForm,
        "general for sale - by owner": PostForm,
        "health and beauty - by owner": PostForm,
        "heavy equipment - by owner": PostForm,
        "household items - by owner": PostForm,
        "jewelry - by owner": PostForm,
        "materials - by owner": PostForm,
        "motorcycle parts - by owner": PostForm,
        "motorcycles/scooters - by owner": PostForm,
        "musical instruments - by owner": PostForm,
        "photo/video - by owner": PostForm,
        "rvs - by owner": PostForm,
        "sporting goods - by owner (no firearms, ammunition, pellet/BB guns, stun guns, etc. )": PostForm,
        "tickets - by owner (one event per posting; please do not sell tickets for more than face value )": PostForm,
        "tools - by owner": PostForm,
        "toys & games - by owner": PostForm,
        "trailers - by owner": PostForm,
        "video gaming - by owner": PostForm,
        "wanted - by owner": PostForm
    },
    "for sale by dealer": {
        "antiques - by dealer": PostForm,
        "appliances - by dealer": PostForm,
        "arts & crafts - by dealer": PostForm,
        "atvs, utvs, snowmobiles - by dealer": PostForm,
        "auto parts - by dealer": PostForm,
        "auto wheels & tires - by dealer": PostForm,
        "baby & kid stuff - by dealer (no illegal sales of recall items, e.g. drop-side cribs, recalled strollers )": PostForm,
        "bicycle parts - by dealer": PostForm,
        "bicycles - by dealer": PostForm,
        "boat parts - by dealer": PostForm,
        "boats - by dealer": PostForm,
        "books & magazines - by dealer": PostForm,
        "business/commercial - by dealer": PostForm,
        "cars & trucks - by dealer (each ad must be for one specific vehicle )": PostForm,
        "cds / dvds / vhs - by dealer": PostForm,
        "cell phones - by dealer": PostForm,
        "clothing & accessories - by dealer": PostForm,
        "collectibles - by dealer": PostForm,
        "computer parts - by dealer": PostForm,
        "computers - by dealer": PostForm,
        "electronics - by dealer": PostForm,
        "farm & garden - by dealer": PostForm,
        "furniture - by dealer": PostForm,
        "general for sale - by dealer": PostForm,
        "health and beauty - by dealer": PostForm,
        "heavy equipment - by dealer": PostForm,
        "household items - by dealer": PostForm,
        "jewelry - by dealer": PostForm,
        "materials - by dealer": PostForm,
        "motorcycle parts - by dealer": PostForm,
        "motorcycles/scooters - by dealer": PostForm,
        "musical instruments - by dealer": PostForm,
        "photo/video - by dealer": PostForm,
        "rvs - by dealer": PostForm,
        "sporting goods - by dealer (no firearms, ammunition, pellet/BB guns, stun guns, etc. )": PostForm,
        "tickets - by dealer (one event per posting )": PostForm,
        "tools - by dealer": PostForm,
        "toys & games - by dealer": PostForm,
        "trailers - by dealer": PostForm,
        "video gaming - by dealer": PostForm,
        "wanted - by dealer": PostForm
    },
    "wanted by owner": PostForm,
    "wanted by dealer": PostForm,
    "service offered": {
        "automotive services": PostForm,
        "beauty services": PostForm,
        "cell phone / mobile services": PostForm,
        "computer services": PostForm,
        "creative services": PostForm,
        "cycle services": PostForm,
        "event services": PostForm,
        "farm & garden services": PostForm,
        "financial services": PostForm,
        "household services": PostForm,
        "labor / hauling / moving": PostForm,
        "legal services": PostForm,
        "lessons & tutoring": PostForm,
        "marine services": PostForm,
        "pet services": PostForm,
        "real estate services": PostForm,
        "skilled trade services": PostForm,
        "small biz ads": PostForm,
        "therapeutic services (non-erotic )": PostForm,
        "travel/vacation services": PostForm,
        "writing / editing / translation": PostForm
    },
    "personal / romance": {
        "missed connection": PostForm,
        "strictly platonic (non-romantic, non-sexual, just friends)": PostForm,
        "dating, romance (long-term relationship)": PostForm,
        "casual encounter (no strings attached)": PostForm,
        "rants and raves": PostForm
    },
    "community": {
        "activity partners": PostForm,
        "artists": PostForm,
        "childcare": PostForm,
        "general community (no politics here please )": PostForm,
        "groups": PostForm,
        "local news and views (no national or international issues here please )": PostForm,
        "lost & found": PostForm,
        "musicians": PostForm,
        "pets (no animal sales or breeding -- rehoming with small adoption fee is ok -- info on free to good home ads )": PostForm,
        "politics": PostForm,
        "rideshare": PostForm,
        "volunteers": PostForm
    },
    "event / class": {
        "I'm selling a small number of tickets to an event": PostForm,
        "My business is having a sale": PostForm,
        "I'm offering an event-related service (rentals, transportation, etc.)": PostForm,
        "I'm advertising a garage sale, estate sale, moving sale, flea market, or other non-corporate sale": ['garage sale', PostForm],
        "I'm advertising a class or training session": PostForm,
        "I'm advertising an event, other than the above": PostForm
    }
}

def home(request):
    result = []
    for column in range(1, 4):
        _result = []
        for mc in Category.objects.filter(parent__isnull=True, column=column):
            cc = Category.objects.filter(parent=mc)
            cc = [ii.name for ii in cc]
            _result += [(mc.name, mc.columns, cc)]
        result += [_result]
    return render(request, 'index.html', {'categories': result})

def login(request):
    return render(request, 'login.html')

def account(request):
    return render(request, 'account.html')

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
