from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView


class LoginUserView(LoginView):
    form_class = AuthenticationForm
    template_name = 'login/login.html'
