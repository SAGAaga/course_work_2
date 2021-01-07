from django.urls import path
from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index_url'),
    path('All_Payments/<int:id>/delete/',
         views.Payment_Delete.as_view(), name='payment_delete'),
    path('Pay/', views.Pay.as_view(), name='pay_url'),
    path('Create_Contract/',
         views.Create_Contract.as_view(), name='create_contract_url'),
    path('All_Payments/<int:id>/edit/',
         views.Edit_Payment.as_view(), name='edit_payment_url'),
    path('All_Contracts/<str:id>/delete/',
         views.Contract_Delete.as_view(), name='contract_delete'),
    path('All_Contracts/<str:id>/edit/',
         views.Edit_Contract.as_view(), name='contract_delete'),
    path('Discounts/<int:id>/delete/',
         views.Discount_Delete.as_view(), name='discount_delete_url'),
    path('Discounts/<int:id>/edit/',
         views.Discount_Edit.as_view(), name='edit_discount_url'),
    path('Add_Discount/',
         views.Discount_Add.as_view(), name='add_discount_url'),
    path('Accomodation/<int:id>/edit/',
         views.Accomodation_Edit.as_view(), name='edit_accomodation_url'),
    path('Accomodation/<int:id>/delete',
         views.Accomodation_Delete.as_view(), name='accomodation_delete_url'),
    path('Add_Accomodation/', views.Accomodation_Add.as_view(),
         name='add_accomodation_url'),
    path('Transfer_new_data/', views.Transfer_new_data.as_view(),
         name='transfer_url'),

    path('All_Payments/<int:id>/Report/',
         views.Make_Payment_Report.as_view(), name='payment_report_url'),
    path('All_Contracts/<str:id>/Report/',
         views.Make_Report_Contract.as_view(), name='contract_report_url'),
    path('Automatization/',
         views.Automatization.as_view(), name='automatization_url'),
]
