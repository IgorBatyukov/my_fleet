from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


class LoginUserView(LoginView):
    form_class = AuthenticationForm
    template_name = 'login/login.html'

    def check_user_group(self, group_name):
        return self.request.user.groups.filter(name=group_name).exists()

    def get_success_url(self):
        if self.check_user_group('crewing_manager'):
            return reverse_lazy('crewing_home')
