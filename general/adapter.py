from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class MyAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        default_site = request.user.default_site
        path = '/'
        if default_site:
            path = "/profile/#" + default_site
        return path


class MySocialAdapter(DefaultSocialAccountAdapter):
	
    def get_connect_redirect_url(self, request, socialaccount):
    	return '/my-account'