# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import json
import stripe
import datetime

from random import randint

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.template.loader import render_to_string
from django.db.models import Q
from django.db.models import Count
from django.apps import apps

from general.models import *
from general.post_models import *
from general.forms import *
from general.utils import send_email, send_SMS

get_class = lambda x: globals()[x]
stripe.api_key = settings.STRIPE_KEYS['API_KEY']

# def index(request):
#     next = request.GET.get('q', '/home')
#     return render(request, 'wraper.html', { 'next': next })

def index(request):
    rndr_str = globoard_display_world_countries()
    return render(request, 'index.html', {'rndr_str': rndr_str})

def about(request):
    return render(request, 'about.html')

def faq(request):
    return render(request, 'faq.html')

def how_it_works(request):
    return render(request, 'how-it-works.html')

def contact_us(request):
    return render(request, 'contact-us.html')

def customer_support(request):
    return render(request, 'customer-support.html')

def why_global_board(request):
    return render(request, 'why-global-board.html')

def terms_of_use(request):
    return render(request, 'terms-of-use.html')

def why_use(request):
    return render(request, 'why-use.html')

@login_required(login_url='/accounts/login/')
def my_ads(request):
    posts = Post.objects.filter(owner=request.user).order_by('-created_at')
    posts = get_posts_with_image(posts)
    return render(request, 'my-ads.html', {'posts': posts})

@csrf_exempt
def search_ads(request):
    keyword = request.POST.get('keyword')
    model = request.POST.get('model')
    others = request.POST.get('others') == 'true'
    view_mode = request.POST.get('view_mode')

    q = Q(title__icontains=keyword)
    if 'ck_search_title' not in request.POST:
        q = (Q(title__icontains=keyword) | Q(content__icontains=keyword))
    q &= (Q(region_id=request.session['region']) | Q(region__district__id=request.session['region']))

    if not others:
        q &= Q(owner=request.user)

    for key, value in request.POST.iteritems():
        if value and key not in ['model', 'keyword', 'others', 'csrfmiddlewaretoken', 'view_mode'] \
        and key[:3] != 'ck_':
            q &= Q(**{key: value})
    
    if model:   # search on specific category page
        q &= Q(category_id=request.session['category'])

    model = apps.get_model('general', model or 'Post')
    posts = model.objects.filter(q).exclude(status='deactive')

    if 'ck_has_image' in request.POST:
        posts = posts.annotate(img_num=Count('images')).filter(img_num__gt=0)
    if 'ck_posted_today' in request.POST:
        posts = posts.filter(created_at__gte=datetime.datetime.now().date())
    
    posts = get_posts_with_image(posts)
    rndr_str = render_to_string(view_mode, {'posts': posts, 'others': others})
    return HttpResponse(rndr_str)

def get_posts_with_image(posts):
    posts_with_image = []
    for post in posts:
        image = Image.objects.filter(post=post).first()
        img_name = image.name if image else 'dummy.jpg'
        posts_with_image.append((post, img_name))
    return posts_with_image

def profile(request):
    return render(request, 'profile.html')

def breadcrumb(request):
    mapName = request.GET.get('mapName')
    state = request.GET.get('state').replace('%27', "'") \
                                    .replace('%20', " ")
    is_state = request.GET.get('is_state')
    city = request.GET.get('city')
    kind = mapName.count('-')

    if city:
        city = City.objects.get(id=city)
        mapname = 'countries/{0}/{0}-all'.format(city.state.country.sortname.lower())
        smapname = mapName + '@' + city.state.name

        if city.district:   # district
            cmapname = smapname + '@' + str(city.district.id)
            dmapname = smapname + '@' + str(city.id)
            args = [mapname, city.state.country.name, 
                    smapname, city.state.name, 
                    cmapname, city.district.name,
                    dmapname, city.name]
        else:
            cmapname = smapname + '@' + str(city.id)
            args = [mapname, city.state.country.name, 
                    smapname, city.state.name, 
                    cmapname, city.name]

    elif kind == 2 or is_state == 'true': # - city
        country = mapName.split('/')[1].upper()
        state = State.objects.filter(name=state, country__sortname=country).first()
        cmapname = 'countries/{0}/{0}-all'.format(state.country.sortname.lower())
        mapname = mapName if '@' in mapName else mapName + '@' + state.name
        args = [cmapname, state.country.name, 
                mapname, state.name]
    elif kind == 1: # state
        country = mapName.split('/')[1].upper()
        country = Country.objects.filter(sortname=country).first()
        args = [mapName, country.name]

    html = render_to_string('_breadcrumb.html', locals())

    request.session['breadcrumb'] = html
    request.session.modified = True

    return HttpResponse(html)

def get_regions(request):
    """
    get regions like countries, states or cities
    and search link, list title
    """
    mapName = request.GET.get('mapName')
    state = request.GET.get('state').replace('%27', "'") \
                                    .replace('%20', " ")
    is_state = request.GET.get('is_state')
    city = request.GET.get('city')
    kind = mapName.count('-')

    if request.user.is_authenticated():
        # store last location
        loc = mapName
        if kind == 2 or is_state == 'true':
            loc += '@' + state 
        if city:
            loc += '@' + city
        request.user.default_site = loc
        request.user.save()

    request.session['category'] = ''

    if city:
        city = City.objects.get(id=city)
        link = '/region-ads/ct/{}'.format(city.id)
        request.session['region'] = city.id
        request.session['region_kind'] = 'city'

        title = 'Select Category'

        result = []
        for column in range(1, 7):
            _result = []
            for mc in Category.objects.filter(parent__isnull=True, column=column).order_by('order'):
                cc = Category.objects.filter(parent=mc).order_by('name')
                _result += [(mc, cc)]
            result += [_result]
        html = render_to_string('_category.html', {'categories': result})            
    elif kind == 2 or is_state == 'true': # - city
        country = mapName.split('/')[1].upper()
        state = State.objects.filter(name=state, country__sortname=country).first()
        title = 'Select City'
        link = '' #'/region-ads/st/{}'.format(state.id)
        request.session['region'] = state.id
        request.session['region_kind'] = 'state'
        cities = City.objects.filter(state=state, district__isnull=True).order_by('name')
        html = render_to_string('_city_list.html', {'cities': cities})
    elif kind == 0: # country
        title = 'Select Country'
        link = ''# '/region-ads/'
        request.session['region'] = ''
        request.session['region_kind'] = 'world'

        html = render_to_string('_country_list_.html', {'countries': Country.objects.all()})
    elif kind == 1: # state
        country = mapName.split('/')[1].upper()
        country = Country.objects.filter(sortname=country).first()
        title = 'Select Region'
        link = ''#'/region-ads/{}'.format(country.id)
        request.session['region'] = country.id
        request.session['region_kind'] = 'country'

        html = render_to_string('_state_list.html', 
                                {'states': State.objects.filter(country=country).order_by('name')})

    request.session.modified = True

    result = {
        'title': title,
        'link': link,
        'html': html
    }

    return JsonResponse(result, safe=False)

@login_required(login_url='/accounts/login/')
def post_ads(request, ads_id):
    if request.method == 'GET':
        mcategories = Category.objects.filter(parent__isnull=True).order_by('name')
        countries = Country.objects.all()
        skey = settings.STRIPE_KEYS['PUBLIC_KEY']

        if ads_id:
            post = Post.objects.get(id=ads_id)
            model = eval(post.category.form)
            post = model.objects.get(id=ads_id)
            states = State.objects.filter(country=post.region.state.country)
            cities = City.objects.filter(state=post.region.state, district__isnull=True)    

            districts = post.region.districts.all()
            if post.region.district:    # for districts
                districts = post.region.district.districts.all()
            
            images = post.images.all()
            detail_template = 'post/{}.html'.format(post.category.form)
        else:
            post = {}       # just for form
            detail_template = 'post/Post.html'

            if request.user.default_site:
                country = request.user.default_site.split('/')[1].upper()
                post['country'] = country       # country sortname
                states = State.objects.filter(country__sortname=country)
                loc = request.user.default_site.split('@')
                if len(loc) > 1:
                    state = loc[1]  # state name
                    post['state'] = state
                    cities = City.objects.filter(state__name=state, district__isnull=True)

                if len(loc) > 2:    # city id
                    city = City.objects.get(id=loc[-1])   
                    districts = city.districts.all()
                    post['region_id'] = city.id

        return render(request, 'post_ads.html', locals())
    else:
        form_name = request.POST.get('ads_form') + 'Form'
        form = get_class(form_name)

        if ads_id:
            model = eval(request.POST.get('ads_form'))
            instance = model.objects.get(id=ads_id)
            form = form(request.POST, instance=instance)
        else:
            form = form(request.POST)

        # ignore last empty one due to template
        images = request.POST.getlist('uploded_id[]')[:-1]  

        if form.is_valid():
            post = form.save()
            pimages = [ii.name for ii in post.images.all()]

            # create objects for new images
            for img in list(set(images)-set(pimages)):
                Image.objects.create(post=post, name=img)

            # remove deleted ones
            for img in list(set(pimages)-set(images)):
                try:
                    os.remove(settings.BASE_DIR+'/static/media/'+img)
                except Exception:
                    pass
                Image.objects.filter(name=img).delete()


            price = int(post.category.price * 100)
            card = request.POST.get('stripeToken')
            if price and card:
                try:
                    stripe.Charge.create(
                        amount=price,
                        currency="usd",
                        source=card, # obtained with Stripe.js
                        description="Charge for Post(#{} - {})".format(post.id, post.title)
                    )
                except Exception, e:
                    print e, 'stripe error ##'
        print(form.errors, '$$$$$$$$')
        return HttpResponseRedirect(reverse('my-ads'))

def ulogout(request):
    logout(request)
    return HttpResponseRedirect('/')

def get_sub_info(request):
    """
    ajax call for sub category, state, city
    """
    obj_id = request.GET.get('obj_id')
    sc_type = request.GET.get('type') # Category, State, City, District
    rndr_str = '<option value="">-Select-</option>'

    if sc_type == 'category':
        for cc in Category.objects.filter(parent__id=obj_id).order_by('name'):
            if cc.category_set.all():
                rndr_str += '<option value="" disabled>{}</option>'.format(cc.name)        
                for sc in cc.category_set.all():
                    rndr_str += '<option value="{}">&nbsp;&nbsp;&nbsp;&nbsp;{}</option>'.format(sc.id, sc.name)        
            else:
                rndr_str += '<option value="{}">{}</option>'.format(cc.id, cc.name)        
        objects = []
    elif sc_type == 'state':
        objects = State.objects.filter(country__id=obj_id)
    elif sc_type == 'city':
        objects = City.objects.filter(state__id=obj_id, district__isnull=True)
    else:
        objects = City.objects.filter(district_id=obj_id)
        
    for sc in objects:
        rndr_str += '<option value="{}">{}</option>'.format(sc.id, sc.name)
    return HttpResponse(rndr_str)

@csrf_exempt
def upload_image(request):
    myfile = request.FILES['images']
    _type = request.POST.get('type', '')
    if _type:
        _type = _type + '/' 

    fs = FileSystemStorage()
    filename = fs.save(_type+myfile.name, myfile)
    uploaded_file_url = fs.url(filename)
    res = {"image_url": uploaded_file_url,"image_name": uploaded_file_url.split('/')[-1]}
    return JsonResponse(res, safe=False)

@csrf_exempt
def delete_image(request):
    image_name = request.POST.get('image_name')
    # if not belong to any post
    if not Image.objects.filter(name=image_name):
        try:
            os.remove(settings.BASE_DIR+'/static/media/'+image_name)
        except Exception:
            pass
    return HttpResponse('')

def get_post_detail(request):
    obj_id = request.GET.get('obj_id')
    category = Category.objects.get(id=obj_id)
    form_name = category.form
    price = int(category.price * 100)
    template = 'post/{}.html'.format(form_name)
    html = render_to_string(template)

    return JsonResponse({
        'html': html, 
        'form': form_name,
        'dealer_avail': category.column == 10,  
        'price': price}, safe=False)

@csrf_exempt
def active_deactive_ads(request):
    ads = request.POST.get('ads_id')
    status = request.POST.get('status')
    Post.objects.filter(id=ads).update(status=status)
    return HttpResponse('')

@csrf_exempt
def delete_ads(request):
    ads = request.POST.get('ads_id')
    Post.objects.filter(id=ads).delete()
    return HttpResponse('')

@csrf_exempt
def delete_camp(request):
    camp = request.POST.get('camp_id')
    Campaign.objects.filter(id=camp).delete()
    return HttpResponse('')

def view_ads(request, ads_id):
    post = get_object_or_404(Post, pk=ads_id)    
    model = eval(post.category.form)
    post = model.objects.get(id=ads_id)

    favourite = False
    result = ''

    if request.user.is_authenticated():
        posts = [ii.post.id for ii in Favourite.objects.filter(owner=request.user)]
        favourite = post.id in posts

    if request.method == 'POST':
        optpay = request.POST.get('optpay')
        contact = request.POST.get('contact')
        card = request.POST.get('stripeToken')
        amount = int(post.price * 100)

        if post.category.form == 'ShortTermPost':
            checkin = request.POST.get('checkin')
            checkout = request.POST.get('checkout')
            adults = request.POST.get('adults')
            children = request.POST.get('children')
            infants = request.POST.get('infants')
            checkin = datetime.datetime.strptime(checkin, '%m/%d/%Y')
            checkin = datetime.datetime.strftime(checkin, '%a %b %d %Y')
            checkout = datetime.datetime.strptime(checkout, '%m/%d/%Y')
            checkout = datetime.datetime.strftime(checkout, '%a %b %d %Y')

            calendar = json.loads(post.calendar)
            calendar.append({
                'start': checkin,
                'end': checkout,
                'avail': False,
                'color': '#ff9800',
                'url': 'http://{}/user_show/{}'.format(settings.ALLOWED_HOSTS[0], request.user.id),
                'title': '{} {} - {}/{}/{}'.format(request.user.first_name, 
                                                 request.user.last_name,
                                                 adults,
                                                 children,
                                                 infants)
            })
            post.calendar = json.dumps(calendar)
            post.save()

        try:
            if optpay == "direct":
                stripe_account_id = '' 
                # SocialAccount.objects.get(user__id=campaign.owner.id, provider='stripe').uid
                app_fee = 0.3

                charge = stripe.Charge.create(
                    amount=amount,
                    currency="usd",
                    source=card, # obtained with Stripe.js
                    # destination=stripe_account_id,
                    # application_fee = int(amount * app_fee),                
                    description="Direct pay to the ads (#{} - {})".format(post.id, post.title)
                )
            else:
                stripe_account_id = '' 
                # SocialAccount.objects.get(user__id=campaign.owner.id, provider='stripe').uid
                app_fee = 0.3

                charge = stripe.Charge.create(
                    amount=amount,
                    currency="usd",
                    source=card, # obtained with Stripe.js
                    # destination=stripe_account_id,
                    # application_fee = int(amount * app_fee),                
                    description="Escrow for the ads (#{} - {})".format(post.id, post.title)
                )

            result = charge.id

            PostPurchase.objects.create(post=post,
                                        purchaser=request.user,
                                        type=optpay,
                                        contact=contact,
                                        transaction=charge.id)
        except Exception as e:
            print e, '@@@@@ Error in view_ads()'

    return render(request, 'ads_detail.html', {
        'post': post,
        'favourite': favourite,
        'reviews': Review.objects.filter(post__id=ads_id),
        'skey': settings.STRIPE_KEYS['PUBLIC_KEY'],
        'result': result
    })

def view_campaign(request, camp_id):
    campaign = Campaign.objects.get(id=camp_id)
    perks = Perk.objects.filter(campaign=campaign)
    result = ''

    if request.method == 'POST':
        perk = request.POST.get('perk_id') or -1
        contact = request.POST.get('contact')
        amount = request.POST.get('amount')
        claimer = request.user if request.user.is_authenticated() else None
        card = request.POST.get('stripeToken')

        perk = Perk.objects.filter(id=perk).first()

        try:
            stripe_account_id = '' 
            # SocialAccount.objects.get(user__id=campaign.owner.id, provider='stripe').uid
            app_fee = 0.3

            charge = stripe.Charge.create(
                amount=amount,
                currency="usd",
                source=card, # obtained with Stripe.js
                # destination=stripe_account_id,
                # application_fee = int(amount * app_fee),                
                description="Contribute to the Campaign (#{} - {})".format(campaign.id, campaign.title)
            )
    
            PerkClaim.objects.create(campaign_id=camp_id,
                                     perk=perk,
                                     contact=contact,
                                     claimer=claimer,
                                     amount=amount,
                                     transaction=charge.id)
            # send notification email to the owner
            if perk:
                subject = 'Perk Claimatoin from Globalboard'
                content = "Perk ({}) in the campaign ({}) is claimed<br><br>Contact Info:<br>" \
                          .format(perk.title, campaign.title)

                # update perk's claimed count, used for cache for less db transaction
                perk.num_claimed = perk.num_claimed + 1
                perk.save()
            else:
                subject = 'Donation to your campaign on Globalboard'
                content = "Donation (${}) is made to the campaign ({})<br><br>Contact Info:<br>" \
                          .format(int(amount)/100, campaign.title)

            content += contact
            send_email(settings.FROM_EMAIL, subject, campaign.owner.email, content)

            # update campaign's raised amount, used for cache for less db transaction
            campaign.raised = campaign.raised + int(amount) / 100
            campaign.save()

            result = charge.id
        except Exception, e:
            print e, 'stripe error ##'
            # result = 'failed'

        
    return render(request, 'camp_detail.html', {
        'post': campaign,
        'perks': perks,
        'skey': settings.STRIPE_KEYS['PUBLIC_KEY'],
        'result': result
    })

def category_ads(request, category_id):
    # store category
    request.session['category'] = category_id
    request.session.modified = True

    category = Category.objects.get(id=category_id)

    tpl_map = {
        10: 'choose_dealer_class.html',
        30: 'disclaimer.html'
    }

    if category.column in tpl_map:    
        return render(request, tpl_map[category.column], {'category': category})
    return category_ads_dealer(request, category_id, 'all')

def category_ads_dealer(request, category_id, kind):
    region_id = request.session.get('region')  # city
    if not region_id:
        return HttpResponseRedirect('/profile')
    region = City.objects.get(id=region_id)

    category = Category.objects.get(id=category_id)
    form = get_class(category.form+'Form')
    posts = Post.objects.filter(Q(region=region) | Q(region__district=region)) \
                        .filter(category_id=category_id).exclude(status='deactive') \
                        .order_by('-created_at')
    if kind == 'owner':
        posts = posts.filter(by_dealer=False)
    elif kind == 'dealer':
        posts = posts.filter(by_dealer=True)

    posts = get_posts_with_image(posts)
    breadcrumb = '<a class="breadcrumb-item" href="javascript:void();" data-mapname="custom/world">worldwide</a>'
    breadcrumb = request.session.get('breadcrumb', breadcrumb)

    return render(request, 'ads-list.html', {
        'posts': posts,
        'region': region,
        'category': category,
        'others': True,
        'breadcrumb': breadcrumb,
        'skey': settings.STRIPE_KEYS['PUBLIC_KEY']
    })

@csrf_exempt
def send_friend_email(request):
    from_email = request.POST.get('from_email')
    to_email = request.POST.get('to_email')
    ads_id = request.POST.get('ads_id')
    post = Post.objects.get(id=ads_id)
    content = """
        {} forwarded you this from craigslist:<br><br>
        <h3>{}</h3><br><br>
        http://18.216.225.192/ads/{}
        """.format(from_email, post.title, post.id)

    send_email(settings.FROM_EMAIL, post.title, to_email, content)
    return HttpResponse('')

@csrf_exempt
def send_reply_email(request):
    from_email = request.POST.get('from_email')
    content = request.POST.get('content')
    ads_id = request.POST.get('ads_id')
    post = Post.objects.get(id=ads_id)

    subject = 'Reply to ' + post.title
    content = """
        {} <br><br>Original post: 
        http://18.216.225.192/ads/{}
        """.format(content, post.id)

    # print (from_email, subject, post.owner.email, content)
    send_email(from_email, subject, post.owner.email, content)
    return HttpResponse('')

def region_ads(request, region_id, region):
    if region == 'city':
        posts = Post.objects.filter(Q(region_id=region_id) | Q(region__district__id=region_id))
    elif region == 'state':    
        posts = Post.objects.filter(region__state__id=region_id)
    elif region == 'world':
        posts = Post.objects.all()

    posts = get_posts_with_image(posts.exclude(status='deactive').order_by('-created_at'))
    breadcrumb = '<a class="breadcrumb-item" href="javascript:void();" data-mapname="custom/world">worldwide</a>'
    breadcrumb = request.session.get('breadcrumb', breadcrumb)

    return render(request, 'ads-list.html', {
        'posts': posts,
        'region': region_id,
        'others': True,
        'breadcrumb': breadcrumb
    })

def globoard_display_world_countries(css_class=''):
    rndr_str = render_to_string('_country_list.html', {
        'css_class': css_class,
        'countries': Country.objects.all()
    })

    return rndr_str

@csrf_exempt
def toggle_favourite(request):
    ads_id = request.POST.get('ads_id')
    res = 'success'
    if request.user.is_authenticated():
        if Favourite.objects.filter(owner=request.user, post_id=ads_id):
            Favourite.objects.filter(owner=request.user, post_id=ads_id).delete()
        else:
            Favourite.objects.create(owner=request.user, post_id=ads_id)
    else:
        res = 'fail'

    return HttpResponse(res)

@login_required(login_url='/accounts/login/')
def my_favourites(request):
    posts = [ii.post for ii in Favourite.objects.filter(owner=request.user)]
    posts = get_posts_with_image(posts)
    return render(request, 'ads-list.html', { 'posts': posts, 
                                              'others': True,
                                              'no_subscription': True})

@login_required(login_url='/accounts/login/')
def my_subscriptions(request):
    searches = Search.objects.filter(owner=request.user)

    return render(request, 'my-subscription.html', {
        'searches': searches
    })

@login_required(login_url='/accounts/login/')
def edit_subscription(request, ss_id):
    categories = []
    states = []
    cities = []

    subscription = Search.objects.get(id=ss_id)
    if subscription.category:
        categories = subscription.category.parent.category_set.all()
    if subscription.state:
        states = subscription.state.country.state_set.all()
    if subscription.city:
        cities = subscription.city.state.city_set.all()

    if request.method == 'GET':
        form = SearchForm(instance=subscription)
    else:
        form = SearchForm(request.POST, instance=subscription)
        if form.is_valid():
            form.save()

            # charge for update
            # card = request.POST.get('stripeToken')
            # try:
            #     stripe.Charge.create(
            #         amount=50,
            #         currency="usd",
            #         source=card, # obtained with Stripe.js
            #         description="Charge for subscription({}) update".format(subscription.keyword)
            #     )
            # except Exception, e:
            #     print e, 'stripe error ##'

            return HttpResponseRedirect(reverse('my-subscriptions'))

    return render(request, 'subscription-edit.html', {
        'form': form,
        'categories': categories,
        'states': states,
        'cities': cities,
        'skey': settings.STRIPE_KEYS['PUBLIC_KEY'],
    })

@csrf_exempt
def create_subscription(request):
    keyword = request.POST.get('keyword')
    category = request.session['category']
    region_kind = request.session['region_kind']
    region_id = request.session['region']

    if region_kind == 'state':
        Search.objects.create(**{
            'owner': request.user,
            'keyword': keyword,
            'category_id': category,
            'state_id': region_id,
            'search_title': request.POST.get('search_title') == 'true',
            'has_image': request.POST.get('has_image') == 'true',
            'min_price': request.POST.get('min_price') or None,
            'max_price': request.POST.get('max_price') or None
        })
    else:
        Search.objects.create(**{
            'owner': request.user,
            'keyword': keyword,
            'category_id': category,
            'city_id': region_id,
            'search_title': request.POST.get('search_title') == 'true',
            'has_image': request.POST.get('has_image') == 'true',
            'min_price': request.POST.get('min_price') or None,
            'max_price': request.POST.get('max_price') or None
        })

    # charge for create
    card = request.POST.get('stripeToken')
    try:
        stripe.Charge.create(
            amount=200,
            currency="usd",
            source=card, # obtained with Stripe.js
            description="Charge for creation of new subscription({})".format(keyword)
        )
    except Exception, e:
        print e, 'stripe error ##'

    return HttpResponse('')

@csrf_exempt
def remove_subscription(request):
    sub_id = request.POST.get('sub_id')

    Search.objects.filter(id=sub_id).delete()
    return HttpResponse('')

@login_required(login_url='/accounts/login/')
def my_account(request):
    dpurchases = PostPurchase.objects.filter(purchaser=request.user, status=0) \
                                     .order_by('created_at')
    ppurchases = PostPurchase.objects.filter(purchaser=request.user).exclude(status=0) \
                                     .order_by('created_at')

    categories = Review.objects.filter(post__owner=request.user) \
                               .values('post__category__name', 'post__category__parent__name', 
                                       'post__category__id') \
                               .distinct()

    for ii in categories:
        ii['reviews'] = Review.objects.filter(post__owner=request.user, 
                                              post__category__id=ii['post__category__id'])
    if request.method == 'GET':
        form = CustomerForm(instance=request.user)
    else:
        form = CustomerForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()

    return render(request, 'my-account.html', {
        'host': request.user,
        'form': form,
        'reviews': categories,
        'dpurchases': dpurchases,
        'ppurchases': ppurchases,
        'num_reviews': Review.objects.filter(post__owner=request.user).count(),
        'stripe': request.user.socialaccount_set.filter(provider='stripe')
    })

@csrf_exempt
def send_vcode(request):
    phone = request.POST.get('phone')
    vcode = randint(100000, 999999)
    print vcode, '###'
    body = "{} is your Globalboard verification code.".format(vcode)
    result = send_SMS(phone, body)

    if result:
        request.session['vcode'] = str(vcode)
        request.session['phone'] = phone        
        request.session.modified = True    
        return HttpResponse('success')
    else:
        return HttpResponse('fail')

@csrf_exempt
def verify_phone(request):
    code = request.POST.get('vcode')
    vcode = request.session['vcode']

    if code == vcode:
        request.user.phone_verified = True
        request.user.phone = request.session['phone']        
        request.user.save()
        return HttpResponse('success')
    else:
        return HttpResponse('fail')

@csrf_exempt
def upload_id(request):
    id_photo = request.POST.get('id_photo')
    request.user.v_statue = 'awaiting_approve'
    # send an email to administrator
    content = """user {} uploaded his ID.<br> Please check and approve it 
                 <a href="http://18.216.225.192/admin/general/customer/{}/change/">here</a>.                 
    """.format(request.user.username, request.user.id)

    send_email(settings.FROM_EMAIL, 'Verification Submitted', settings.ADMIN_EMAIL, content)
    request.user.id_photo = 'ID/' + id_photo
    request.user.save()
    return HttpResponse('')

def confirm_phone(request):
    return render(request, 'account/phone_confirm.html')

@login_required(login_url='/accounts/login/')
def my_campaigns(request):
    campaigns_ = []
    campaigns = Campaign.objects.filter(owner=request.user).order_by('-created_at')

    for ii in campaigns:
        if ii.created_at >= datetime.datetime.now().date() + datetime.timedelta(days=-ii.duration):
            campaigns_.append(ii)

    return render(request, 'my-campaigns.html', {
        'campaigns': campaigns,
        'mine': True
    })

@login_required(login_url='/accounts/login/')
def post_camp(request, camp_id):
    categories = CampCategory.objects.all()
    if request.method == 'GET':
        form = CampaignForm()
    else:
        form = CampaignForm(request.POST, request.FILES)

        if form.is_valid():
            camp = form.save()
            num_perks = int(request.POST.get('num_perks'))
            fs = FileSystemStorage()

            iii = 0
            for ii in range(num_perks):
                filename = None
                if request.POST.getlist('flag_perk_overview')[ii]:
                    perk_img = request.FILES.getlist('perk_overview')[iii]
                    filename = fs.save('perks/'+perk_img.name, perk_img)
                    iii += 1

                Perk.objects.create(title=request.POST.getlist('perk_title')[ii],
                                    campaign=camp,
                                    price=request.POST.getlist('perk_price')[ii],
                                    description=request.POST.getlist('perk_desc')[ii],
                                    num_avail=request.POST.getlist('perk_avail_num')[ii] or 1000000,
                                    image=filename)

            return HttpResponseRedirect(reverse('my-campaigns'))
        print(form.errors, '$$$$$$$$')
    return render(request, 'post_camp.html', {
        'form': form,
        'categories': categories,   
        'rng_perks': range(1, 11)
    })

def explorer_campaigns(request):
    categories = CampCategory.objects.all()
    campaigns = Campaign.objects.all().order_by('-created_at')

    return render(request, 'campaign-list.html', {
        'categories': categories,
        'campaigns': campaigns
    })

@csrf_exempt
def search_camps(request):
    keyword = request.POST.get('keyword')
    category = request.POST.get('category')
    others = request.POST.get('others')

    # if others:
        # .filter(owner=request.user)
    campaigns = Campaign.objects.filter(Q(title__icontains=keyword) 
                                      | Q(overview__icontains=keyword) 
                                      | Q(tagline__icontains=keyword))
    if category:
        campaigns = campaigns.filter(Q(category=category) | Q(category__parent=category))

    campaigns_ = []
    for ii in campaigns:
        if ii.created_at >= datetime.datetime.now().date() + datetime.timedelta(days=-ii.duration):
            campaigns_.append(ii)

    rndr_str = render_to_string('_camp_list.html', {'campaigns': campaigns_})
    return HttpResponse(rndr_str)

@csrf_exempt
def rate_ads(request):
    Review.objects.create(post_id=request.POST.get('post_id'),
                          rater=request.user,
                          rating=request.POST.get('rating'),
                          content=request.POST.get('content'))

    return HttpResponse('')

def user_show(request, user_id):
    host = Customer.objects.get(id=user_id)
    categories = Review.objects.filter(post__owner=host) \
                               .values('post__category__name', 'post__category__parent__name', 
                                       'post__category__id') \
                               .distinct()
    for ii in categories:
        ii['reviews'] = Review.objects.filter(post__owner=host, 
                                              post__category__id=ii['post__category__id'])

    return render(request, 'user_show.html', { 
        'host': host,
        'reviews': categories,
        'num_reviews': Review.objects.filter(post__owner=host).count()
    })

@csrf_exempt
def release_purchase(request):
    p_id = request.POST.get('p_id')
    purchase = PostPurchase.objects.get(id=p_id)

    # send money to the post's owner
    amount = int(purchase.post.price * 100)
    app_fee = 0.3

    transfer = stripe.Transfer.create(
        amount=amount,
        currency="usd",
        source_transaction=purchase.transaction,
        destination=purchase.post.owner.socialaccount_set.get(provider='stripe').uid,
    )

    purchase.status = 0
    purchase.transaction = transfer.id
    purchase.save()

    return HttpResponse(transfer.id)
    
@csrf_exempt    
def update_alert(request):
    sid = request.POST.get('sid')
    alert = request.POST.get('alert') == 'true'
    Search.objects.filter(id=sid).update(alert=alert)
    return HttpResponse('')
