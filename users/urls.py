

from django.urls import path,include
from django.conf.urls import url
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    #website
    path('login/',csrf_exempt(login),name='login'),
    path('users/',usersListView.as_view(),name='users'),
    path('clients/',clientsListView.as_view(),name='clients'),
    path('firms/',firmsListView.as_view(),name='firms'),
    path('lawyers/',lawyersListView.as_view(),name='lawyers'),
    path('cases/',casesListView.as_view(),name='cases'),
    path('register_client/',register_client.as_view(),name='register_client'),
    path('register_firm/',register_firm.as_view(),name='register_firm'),
    path('register_lawyer/',register_lawyer.as_view(),name='register_lawyer'),
]