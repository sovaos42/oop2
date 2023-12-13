from django.urls import path
from . import views
from django.urls import re_path as url
from .models import Application

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^register/$', views.register, name='register'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^application/$', views.ApplicationList.as_view(), name='application'),
    url(r'^application/create/$', views.ApplicationCreate.as_view(), name='application-create'),
    url(r'^application/(?P<pk>\d+)/delete/$', views.ApplicationDelete.as_view(), name='application-delete'),
    path(r'^application/(?P<pk>\w+)/(?P<st>\w+)/update/$', views.confirm_update, name='confirm-update'),
    url(r'^application/application_admin/$', views.ApplicationListAdmin.as_view(), name='application-admin'),
    path('view_categories', views.ViewCategory.as_view(), name='view-categories'),
    path('view_categories/create_category', views.CreateCategory.as_view(), name='create-category'),
    url(r'^category/(?P<pk>\d+)/delete/$', views.DeleteCategory.as_view(), name='delete-category'),
]
