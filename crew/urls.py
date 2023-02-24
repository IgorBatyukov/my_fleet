from django.urls import path, register_converter, re_path
from crew import views, converters

register_converter(converters.DateConverter, 'date')

urlpatterns = [

    path('', views.CrewingMainView.as_view(), name='crewing_home'),
    path('vessels/', views.VesselsMainView.as_view(), name='crewing_vessels'),
    path('vessels/<int:pk>', views.VesselDetailsView.as_view(), name='vessel_details'),
    path('crew/', views.CrewListView.as_view(), name='crew'),
    path('crew/<int:pk>', views.CrewDetailsView.as_view(), name='crew_member_details'),
    path('crewchange/', views.CrewChangeView.as_view(), name='crew_change'),
    path('crewchange/<str:vessel__name>/<date:date>/<str:port__name>/<str:type>',
         views.CrewChangeDetailsView.as_view(),
         name='crew_change_details'),

]
