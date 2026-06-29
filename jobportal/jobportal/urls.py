"""
URL configuration for jobportal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from job import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
path('', views.index,name='index'),
    path('admin_login',views.admin_login,name='admin_login'),
    path('recruiter_login',views.recruiter_login,name='recruiter_login'),
    path('user_login',views.user_login,name='user_login'),
    path('user_signup',views.user_signup,name='user_signup'),
    path('user_home',views.user_home,name='user_home'),
    path('recruiter_home', views.recruiter_home, name='recruiter_home'),
    path('admin_home',views.admin_home,name='admin_home'),
path('recruiter_signup',views.recruiter_signup,name='recruiter_signup'),
    path('view_users',views.view_users,name='view_users'),
    path('delete_user/<int:id>',views.delete_user,name='delete_user'),
    path('change_status/<int:id>', views.change_status, name='change_status'),
    path('recruiter_pending',views.recruiter_pending,name='recruiter_pending'),
    path('recruiter_accepted', views.recruiter_accepted, name='recruiter_accepted'),
path('recruiter_rejected', views.recruiter_rejected, name='recruiter_rejected'),
path('view_recruiters', views.view_recruiters, name='view_recruiters'),
    path('delete_recruiter/<int:id>', views.delete_recruiter, name='delete_recruiter'),
    path('adminchange_password',views.adminchange_password,name='adminchange_password'),
    path('applicantchange_password', views.applicantchange_password, name='applicantchange_password'),
    path('recruiterchange_password', views.recruiterchange_password, name='recruiterchange_password'),
    path('addjob',views.addjob,name='addjob'),
    path('job_list', views.job_list, name='job_list'),
path('editjob/<int:id>', views.editjob, name='editjob'),
    path('changecompanylogo/<int:id>',views.changecompanylogo,name='changecompanylogo'),
    path('latestjobs',views.latestjobs,name='latestjobs'),
    path('userjobs',views.userjobs,name='userjobs'),
path('jobdetails/<int:id>',views.jobdetails,name='jobdetails'),
path('applyjob/<int:id>',views.applyjob,name='applyjob'),
    path('candidates',views.candidates,name='candidates'),
    path('delete_candidates/<int:id>', views.delete_candidates, name='delete_candidates'),
path('contact',views.contact,name='contact'),
path('view_contacts', views.view_contacts, name='view_contacts'),

    path('Logout',views.Logout,name='Logout'),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.conf.urls.static import static
from django.conf import settings

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

