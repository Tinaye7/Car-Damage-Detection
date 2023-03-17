
from django.contrib import admin
from django.urls import path
from insurance import views
from insurance import app
from django.contrib.auth.views import LogoutView,LoginView
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),


    path('customer/',include('customer.urls')),
    path('',views.home_view,name=''),
    path('logout', LogoutView.as_view(template_name='insurance/logout.html'),name='logout'),
    path('aboutus', views.aboutus_view),
    path('contactus', views.contactus_view),
    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('customer/afterlogin', views.afterlogin_view,name='afterlogin'),
    
    path('adminlogin', LoginView.as_view(template_name='insurance/adminlogin.html'),name='adminlogin'),
    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),

    path('admin-view-customer', views.admin_view_customer_view,name='admin-view-customer'),
    path('update-customer/<int:pk>', views.update_customer_view,name='update-customer'),
    path('delete-customer/<int:pk>', views.delete_customer_view,name='delete-customer'),

    path('admin-category', views.admin_category_view,name='admin-category'),
    path('admin-view-category', views.admin_view_category_view,name='admin-view-category'),
    path('admin-update-category', views.admin_update_category_view,name='admin-update-category'),
    path('update-category/<int:pk>', views.update_category_view,name='update-category'),
    path('admin-add-category', views.admin_add_category_view,name='admin-add-category'),
    path('admin-delete-category', views.admin_delete_category_view,name='admin-delete-category'),
    path('delete-category/<int:pk>', views.delete_category_view,name='delete-category'),


    path('admin-policy', views.admin_policy_view,name='admin-policy'),
    path('admin-add-policy', views.admin_add_policy_view,name='admin-add-policy'),
    path('admin-view-policy', views.admin_view_policy_view,name='admin-view-policy'),
    path('admin-update-policy', views.admin_update_policy_view,name='admin-update-policy'),
    path('update-policy/<int:pk>', views.update_policy_view,name='update-policy'),
    path('admin-delete-policy', views.admin_delete_policy_view,name='admin-delete-policy'),
    path('delete-policy/<int:pk>', views.delete_policy_view,name='delete-policy'),

    path('admin-view-policy-holder', views.admin_view_policy_holder_view,name='admin-view-policy-holder'),
    path('admin-view-approved-claims', views.admin_view_approved_claims_view,name='admin-view-approved-claims'),
    path('admin-view-disapproved-claims', views.admin_view_disapproved_claims_view,name='admin-view-disapproved-claims'),
    path('admin-view-waiting-claims', views.admin_view_waiting_claims_view,name='admin-view-waiting-claims'),
    path('approve-request/<int:pk>', views.approve_request_view,name='approve-request'),
    path('reject-request/<int:pk>', views.disapprove_request_view,name='reject-request'),

    path('admin-question', views.admin_question_view,name='admin-question'),
    path('update-question/<int:pk>', views.update_question_view,name='update-question'),
    
    #path('multipleform', views.multipleform, name='multipleform'),
    #path('multipleform_save', views.multipleform_save, name='multipleform_save'),
    path('assessment',app.assess,name='assessment'),
    path('assessment2',app.upload_and_classify,name='assessment2'),
    path('claims',views.claims,name='claims'),
    #path('profile_pic',views.profile,name='profile_pic'),
    path('assess_claim/<int:pk>',views.assess_claim,name='assess_claim'),
    path('customer/claim_details/<int:pk>',views.claim_details,name='claim_details')
]
