from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('test/', testfunc, name='test'),
    path('list/', listfunc, name='list'),
    path('signup/', signupfunc, name='signup'),
    path('login/', loginfunc, name='login'),
    path('logout/', logoutfunc, name='logout'),
    path('', hwfunc),
    path('profile/', profilefunc, name='profile'),
    path('upload/', uploadfunc, name='upload'),
    path('detail/<int:pk>', detailfunc, name='detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)