from django.urls import path
from crew import views


urlpatterns = [

    path('crewing', views.CrewingMainView.as_view()),
    path('crewing/vessels', views.VesselsMainView.as_view()),
    path('crewing/vessels/<int:vsl_id>', views.VesselDetailsView.as_view()),
    path('crewing/crew', views.CrewingMainView.as_view()),
    path('crewing/crew/<int:pk>', views.CrewDetailsView.as_view()),

]
