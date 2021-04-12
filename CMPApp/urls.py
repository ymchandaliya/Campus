from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',home,name='home'),
    path('signup',signup,name='signup'),
    path('login',login,name='login'),
    path('profile',profile,name='profile'),
    path('contact',contact,name='contact'),
    path('logout',logout,name='logout'),
    path('faq',faq,name='faq'),
    path('dashboard',dashboard,name='dashboard'),
    path('newrequests',newrequests,name='newrequests'),
    path('ajax/validate_username/$/',validate_username,name='validate_username'),
    path('emailverification/<str:ver>/',emailverification,name='emailverfication'),
    path('share',share,name='share'),
    path('upload',upload,name='upload'),
    #for testing
    path('display',display,name='display'),
    path('details',details,name='details'),
    path('search',search,name='search'),
    path('details/<int:id>/',details,name='details'),
    path('deletebook/<int:id>/',deletebook,name='deletebook'),
    path('delreq/<int:id>/',delreq,name='delreq'),
    path('deletenew/<int:id>/',deletenew,name='deletenew'),
    path('approve/<int:id>/',approve,name='approve'),
    path('reject/<int:id>/',reject,name='reject'),
    path('details1/',details1,name='details1'),
    path('suggest',suggest,name='suggest'),
    # path('approved/<int:id>',approved,name='approved'),
    # # path('disapproved/<int:id>',disapproved,name='disapproved'),
    # path('DashBoard/<email>',DashBoard,name='DashBoard'),
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
