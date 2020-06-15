from django.conf.urls import url
from django.urls import path
from . import views

# SET THE NAMESPACE!
app_name = 'pluton'
# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    url(r'^register/$',views.register,name='register'),
    url(r'^user_login/$',views.user_login,name='user_login'),
    url(r'^$',views.index,name='index'),
    url(r'^special/',views.special,name='special'),
    url(r'^home/$',views.home,name='home'),
    url(r'^culturals/$',views.culturals,name='culturals'),
    url(r'^scitech/$',views.scitech,name='scitech'),
    url(r'^sports/$',views.sports,name='sports'),
    url(r'^artlit/$',views.artlit,name='artlit'),
    url(r'^streetplay/$',views.streetplay,name='streetplay'),
    url(r'^westernband/$',views.westernband,name='westernband'),
    url(r'^photography/$',views.photography,name='photography'),
    url(r'^hackathon/$',views.hackathon,name='hackathon'),
    url(r'^sciencequiz/$',views.sciencequiz,name='sciencequiz'),
    url(r'^ctf/$',views.ctf,name='ctf'),
    url(r'^about/$',views.about,name='about'),
    url(r'^chess/$',views.chess,name='chess'),
    url(r'^chatbot/$',views.chatbot,name='chatbot'),
    url(r'^basketball/$',views.basketball,name='basketball'),
    url(r'^themepaint/$',views.themepaint,name='themepaint'),
    url(r'^creativewriting/$',views.creativewriting,name='creativewriting'),

    url(r'^registerevent1/$',views.registerevent1,name='registerevent1'),
    url(r'^payment/$', views.payment, name='payment'),
   
    url(r'^succ/$',views.succ,name='succ'),
    url(r'^logout/$', views.user_logout, name='logout'),
    #path('subscribe/', views.subscribe, name = 'subscribe'),
]


