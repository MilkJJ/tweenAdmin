from django.urls import path
from . import views


urlpatterns = [
    path('firebase', views.index, name='index'),

    #Admin Account
    path('signIn/', views.signIn, name='signIn'),
    path('postsign/', views.postsign, name='postsign'),
    path('logout/', views.logout, name='logout'),

    #Add Health Tips
    path('addTips/',views.addTips,name='addTips'),
    path('tips_add/',views.tips_add,name='tips_add'),

    #Check Health Tips
    path('checkTips/', views.checkTips, name='checkTips'),
    path('tips_check/', views.tips_check, name='tips_check'),
]