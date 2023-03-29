from django.urls import path
from .views import LoginUserView, logout_user


urlpatterns = [

    path('', LoginUserView.as_view(), name='login'),
    path('logout', logout_user, name='logout'),

]