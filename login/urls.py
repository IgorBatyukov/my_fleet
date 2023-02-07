from django.urls import path
from .views import LoginUserView


urlpatterns = [

    path('', LoginUserView.as_view()),

]