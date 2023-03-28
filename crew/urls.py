from django.urls import path, register_converter, re_path
from crew import views, converters

register_converter(converters.DateConverter, 'date')

urlpatterns = [

    path('', views.CrewingMainView.as_view(), name='crewing_home'),
    path('vessels/', views.VesselsMainView.as_view(), name='crewing_vessels'),
    path('vessels/<int:pk>', views.VesselDetailsView.as_view(), name='vessel_details'),
    path('crew/', views.CrewListView.as_view(), name='crew'),
    path('crew/<int:pk>', views.CrewDetailsView.as_view(), name='crew_member_details'),
    path('crew/<int:pk>/edit/', views.CrewDetailsEditView.as_view(), name='crew_personal_edit'),
    path('crew/<int:crew_id>/certificate/<int:pk>/edit/', views.CrewCertificateEdit.as_view(), name='certificate_edit'),
    path('crew/<int:crew_id>/certificate/<int:pk>/delete/', views.CrewCertificateDelete.as_view(), name='certificate_delete'),
    path('crew/<int:crew_id>/certificate/add/', views.CrewCertificateAdd.as_view(), name='certificate_add'),
    path('crewchange/', views.CrewChangeView.as_view(), name='crew_change'),
    path('crewchange/<str:vessel__name>/<date:date>/<str:port__name>/<str:type>',
         views.CrewChangeDetailsView.as_view(),
         name='crew_change_details'),
    path('crewchange/add/', views.CrewChangeAdd.as_view(), name='crew_change_add'),
    path('crewchange/vessel/<int:vessel_id>/add/', views.CrewChangeAddOnVessel.as_view(), name='crew_change_add_on_vessel'),
    path('contracts/', views.ContractMainView.as_view(), name='contracts_list'),
    path('contracts/add/', views.ContractAdd.as_view(), name='contract_add'),
    path('contracts/<int:pk>/edit/', views.ContractEdit.as_view(), name='contract_edit'),

]
