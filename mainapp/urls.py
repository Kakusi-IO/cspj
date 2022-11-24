from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from sql_app.api import api

urlpatterns = [
    path('api/', api.urls, name='api'),
    path('list/', listfunc, name='list'),
    path('signup/', signupfunc, name='signup'),
    path('login/', loginfunc, name='login'),
    path('logout/', logoutfunc, name='logout'),
    path('', hwfunc, name='index'),
    path('profile/', profilefunc, name='profile'),
    path('createtask/', createtaskfunc, name='createtask'),
    path('detail/<int:pk>', detailfunc, name='detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)