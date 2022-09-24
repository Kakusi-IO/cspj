from django.urls import path
from .views import *

urlpatterns = [
    path('list/', TasksList.as_view(), name='list'),
    path('signup/', signupfunc, name='signup'),
    path('login/', loginfunc, name='login'),
    path('logout/', logoutfunc, name='logout'),
    path('', hwfunc)
]
