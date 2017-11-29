from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter

class MyAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        default_site = request.user.default_site
        path = '/'
        if default_site:
            path = "/profile/#" + default_site
        return path

    def save_user(self, request, user, form, commit=False):
        data = form.cleaned_data
        user.email = data['email']
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.gender = data['gender']
        user.dob = data['dob']
        user.address = data['address']

        if 'password1' in data:
            user.set_password(data['password1'])
        else:
            user.set_unusable_password()

        self.populate_username(request, user)

        print user, '########3'
        if commit:
            user.save()
        return user
