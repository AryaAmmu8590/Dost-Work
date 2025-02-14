from django.urls import path
from. import views





urlpatterns = [
    
     path('',views.home,name='home'),
     path('login/',views.login_view,name='login'),
     path('logout/',views.logout_view,name='logout'),
     path('about/',views.about,name='about'),
     path('blog/',views.blog,name='blog'),
     path('contact/',views.contact,name='contact'),
     path('service/',views.service,name='service'),
     
     path('user_registration/',views.user_registration,name='user_registration'),
     path('agency_registration/',views.agency_registration,name='agency_registration'),
     path('worker-registration/',views.worker_registration,name='worker-registration'),
     path('table/',views.table),
     path('signup/',views.signup,name='signup' ),
     path('user_deatails_view/',views.user_deatails_view,name='user_deatails_view'),
     path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),
     path('user_dashboard/',views.user_dashboard,name='user_dashboard'),
     path('agency_dashboard/',views.agency_dashboard,name='agency_dashboard'),
     path('worker/',views.worker,name='worker'),
     path('navbar/',views.navbar,name='navbar'),

     ## dashboards
     path('user_list_workers/',views.user_list_workers,name='user_list_workers'),
     path('user_profile/',views.user_profile,name='user_profile'),
     path('worker_profile/',views.worker_profile,name='worker_profile'),
     path('view_worker_details/<int:worker_id>/',views.view_worker_details,name='view_worker_details'),
     path('review_worker_list/<int:worker_id>/',views.review_list_worker,name='review_worker_list'),
     path('submit_review/<int:worker_id>/',views.submit_review,name='submit_review'),
     path('book_worker/<int:worker_id>/', views.book_worker, name='book_worker'),
     path('worker_view/', views.worker_view, name='worker_view'),
     path('user_view/', views.user_view, name='user_view'),
     path('admin_booking/', views.admin_booking, name='admin_booking'),
     path('user_complaints/',views.user_complaints,name='user_complaints'),
     path('user_details/',views.user_details,name='user_details'),
     path('complaints_replay/',views.complaints_replay,name='complaints_replay'),
     path('agency_profile/',views.agency_profile,name='agency_profile'),
     path('agency_workers/',views.agency_workers,name='agency_workers'),
     path('approve_worker/<int:worker_id>/',views.approve_worker,name='approve_worker'),
     path('reject_worker/<int:worker_id>/',views.reject_worker,name='reject_worker'),
     path('reports', views.reports, name='reports'),
     path('agency_details/', views.agency_details, name='agency_details'),
     path('workers_details/', views.workers_details, name='workers_details'),
     path('new_reg/', views.new_reg, name='new_reg'),
     path('user_complaint/', views.user_complaint, name='user_complaint'),
     path('worker_complaint/', views.worker_complaint, name='worker_complaint'),
     path('worker_dash_com/', views.worker_dash_com, name='worker_dash_com'),
     path('worker_weekly_reports/', views.worker_weekly_reports, name='worker_weekly_reports'),
     path('weekly_worker_reports/', views.weekly_worker_reports, name='weekly_worker_reports'),
     
     path('worker_report/', views.worker_report, name='worker_report'),
     path('admin_noty/', views.admin_noty, name='admin_noty'),
     path('agency_user_replay/<int:complaint_id>/', views.agency_user_replay, name='agency_user_replay'),

     path('agency_worker_replay/', views.agency_worker_replay, name='agency_worker_replay'),
     path('admin_user_report/', views.admin_user_report, name='admin_user_report'),
     path('admin_worker_report/', views.admin_worker_report, name='admin_worker_report'),

     path('payment/', views.payment, name='payment'),
     path('success/', views.success, name='success'),
     path('admin_pay/', views.admin_pay, name='admin_pay'),
     path('email/', views.email, name='email'),






     
     
     
     

]
