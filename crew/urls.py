from django.urls import path
from crew import views


urlpatterns = [

    path('', views.CrewingMainView.as_view(), name='crewing_home'),
    path('vessels/', views.VesselsMainView.as_view(), name='crewing_vessels'),
    path('vessels/<int:pk>', views.VesselDetailsView.as_view(), name='vessel_details'),
    path('crew/', views.CrewingMainView.as_view(), name='crew'),
    path('crew/<int:pk>', views.CrewDetailsView.as_view()),

]
