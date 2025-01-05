from django.urls import path
from. import views





urlpatterns = [
    
     path('',views.home,name='home'),
     path('login/',views.login_view,name='login'),
     path('about/',views.about,name='about'),
     path('blog/',views.blog,name='blog'),
     path('contact/',views.contact,name='contact'),
     path('service/',views.service,name='service'),
     
     path('user_registration/',views.user_registration,name='user_registration'),
     path('agency-registration/',views.agency_registration,name='agency-registration'),
     path('worker-registration/',views.worker_registration,name='worker-registration'),
     path('table/',views.table),
     path('signup/',views.signup,name='signup' ),
     path('user_deatails_view/',views.user_deatails_view,name='user_deatails_view'),
     path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),
     path('user_dashboard/',views.user_dashboard,name='user_dashboard'),
     path('agency_dashboard/',views.agency_dashboard,name='agency_dashboard'),
     path('worker/',views.worker,name='worker')
     
     
     

]
