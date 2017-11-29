from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter

class MyAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        default_site = request.user.default_site
        path = '/'
        if default_site:
            path = "/profile/#" + default_site
        return path

