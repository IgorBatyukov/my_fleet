from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy


class LoginUserView(LoginView):
    form_class = AuthenticationForm
    template_name = 'login/login.html'

    def get_success_url(self):
        if self.request.user.is_authenticated:
            return reverse_lazy('crewing_home')
