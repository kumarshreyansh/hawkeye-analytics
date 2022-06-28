"""hawkeyeproj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include
from modelFormsApp import views as modelFormsAppview

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('home/', modelFormsAppview.home),
    path('coach/', modelFormsAppview.coach),
    #path('listallentries/', modelFormsAppview.listallentries),
    path('addnewentry/', modelFormsAppview.addnewentry),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', modelFormsAppview.logout),
    #path('todaytable/', modelFormsAppview.todaytable),
    path('todayrifle/', modelFormsAppview.todayrifle),
    path('todaypistol/', modelFormsAppview.todaypistol),
    path('todaypistolwomen/', modelFormsAppview.todaypistolwomen),
    path('todaypistolmen/', modelFormsAppview.todaypistolmen),
    path('todayriflewomen/', modelFormsAppview.todayriflewomen),
    path('todayriflemen/', modelFormsAppview.todayriflemen),
    path('monthlypistol/', modelFormsAppview.monthlypistol),
    path('monthlyrifle/', modelFormsAppview.monthlyrifle),
    path('monthlypistolwomen/', modelFormsAppview.monthlypistolwomen),
    path('monthlypistolmen/', modelFormsAppview.monthlypistolmen),
    path('monthlyriflewomen/', modelFormsAppview.monthlyriflewomen),
    path('monthlyriflemen/', modelFormsAppview.monthlyriflemen),
    path('quarterlyrifle/', modelFormsAppview.quarterlyrifle),
    path('quarterlypistol/', modelFormsAppview.quarterlypistol),
    path('quarterlypistolwomen/', modelFormsAppview.quarterlypistolwomen),
    path('quarterlypistolmen/', modelFormsAppview.quarterlypistolmen),
    path('quarterlyriflewomen/', modelFormsAppview.quarterlyriflewomen),
    path('quarterlyriflemen/', modelFormsAppview.quarterlyriflemen),
    path('myprofile/', modelFormsAppview.myprofile),
    path('diary/', modelFormsAppview.diary),
    path('profiles/', modelFormsAppview.profiles),
    path('profilesuser/<str:username>/', modelFormsAppview.profilesuser),
    path('profilesuser40shot_json/<str:username>/', modelFormsAppview.profilesuser40shot_json, name='profilesuser40shot_json'),
    path('profilesuser60shot_json/<str:username>/', modelFormsAppview.profilesuser60shot_json, name='profilesuser60shot_json'),
    path('profilesuserhigheastseriesscore40shot_json/<str:username>/', modelFormsAppview.profilesuserhigheastseriesscore40shot_json, name='profilesuserhigheastseriesscore40shot_json'),
    path('profilesuserhigheastseriesscore60shot_json/<str:username>/', modelFormsAppview.profilesuserhigheastseriesscore60shot_json, name='profilesuserhigheastseriesscore60shot_json'),
    path('profilesusernumberoftens40shot_json/<str:username>/', modelFormsAppview.profilesusernumberoftens40shot_json, name='profilesusernumberoftens40shot_json'),
    path('profilesusernumberoftens60shot_json/<str:username>/', modelFormsAppview.profilesusernumberoftens60shot_json, name='profilesusernumberoftens60shot_json'),
    path('profilesusercancellationofbadshot40shot_json/<str:username>/', modelFormsAppview.profilesusercancellationofbadshot40shot_json, name='profilesusercancellationofbadshot40shot_json'),
    path('profilesusercancellationofbadshot60shot_json/<str:username>/', modelFormsAppview.profilesusercancellationofbadshot60shot_json, name='profilesusercancellationofbadshot60shot_json'),
    path('profilesuserstabilityofsightpicture40shot_json/<str:username>/', modelFormsAppview.profilesuserstabilityofsightpicture40shot_json, name='profilesuserstabilityofsightpicture40shot_json'),
    path('profilesuserstabilityofsightpicture60shot_json/<str:username>/', modelFormsAppview.profilesuserstabilityofsightpicture60shot_json, name='profilesuserstabilityofsightpicture60shot_json'),
    path('profilesuserbodybalance40shot_json/<str:username>/', modelFormsAppview.profilesuserbodybalance40shot_json, name='profilesuserbodybalance40shot_json'),
    path('profilesuserbodybalance60shot_json/<str:username>/', modelFormsAppview.profilesuserbodybalance60shot_json, name='profilesuserbodybalance60shot_json'),
    path('profilesuserflowoftheshot40shot_json/<str:username>/', modelFormsAppview.profilesuserflowoftheshot40shot_json, name='profilesuserflowoftheshot40shot_json'),
    path('profilesuserflowoftheshot60shot_json/<str:username>/', modelFormsAppview.profilesuserflowoftheshot60shot_json, name='profilesuserflowoftheshot60shot_json'),
    path('profilesuserninetydegreetriggeroperation40shot_json/<str:username>/', modelFormsAppview.profilesuserninetydegreetriggeroperation40shot_json, name='profilesuserninetydegreetriggeroperation40shot_json'),
    path('profilesuserninetydegreetriggeroperation60shot_json/<str:username>/', modelFormsAppview.profilesuserninetydegreetriggeroperation60shot_json, name='profilesuserninetydegreetriggeroperation60shot_json'),
    path('profilesuseraverageshotduration40shot_json/<str:username>/', modelFormsAppview.profilesuseraverageshotduration40shot_json, name='profilesuseraverageshotduration40shot_json'),
    path('profilesuseraverageshotduration60shot_json/<str:username>/', modelFormsAppview.profilesuseraverageshotduration60shot_json, name='profilesuseraverageshotduration60shot_json'),
    path('profilesuserfollowthrough40shot_json/<str:username>/', modelFormsAppview.profilesuserfollowthrough40shot_json, name='profilesuserfollowthrough40shot_json'),
    path('profilesuserfollowthrough60shot_json/<str:username>/', modelFormsAppview.profilesuserfollowthrough60shot_json, name='profilesuserfollowthrough60shot_json'),
    path('profilesuservisualization40shot_json/<str:username>/', modelFormsAppview.profilesuservisualization40shot_json, name='profilesuservisualization40shot_json'),
    path('profilesuservisualization60shot_json/<str:username>/', modelFormsAppview.profilesuservisualization60shot_json, name='profilesuservisualization60shot_json'),
    path('profilesusermentalstability40shot_json/<str:username>/', modelFormsAppview.profilesusermentalstability40shot_json, name='profilesusermentalstability40shot_json'),
    path('profilesusermentalstability60shot_json/<str:username>/', modelFormsAppview.profilesusermentalstability60shot_json, name='profilesusermentalstability60shot_json'),
    path('profilesuserhydrationlevel40shot_json/<str:username>/', modelFormsAppview.profilesuserhydrationlevel40shot_json, name='profilesuserhydrationlevel40shot_json'),
    path('profilesuserhydrationlevel60shot_json/<str:username>/', modelFormsAppview.profilesuserhydrationlevel60shot_json, name='profilesuserhydrationlevel60shot_json'),
    path('profilesuserfueling40shot_json/<str:username>/', modelFormsAppview.profilesuserfueling40shot_json, name='profilesuserfueling40shot_json'),
    path('profilesuserfueling60shot_json/<str:username>/', modelFormsAppview.profilesuserfueling60shot_json, name='profilesuserfueling60shot_json'),    
    path('myprofile_monthlyscore40shot_json/', modelFormsAppview.myprofile_monthlyscore40shot_json, name='myprofile_monthlyscore40shot_json'),
    path('myprofile_monthlyscore60shot_json/', modelFormsAppview.myprofile_monthlyscore60shot_json, name='myprofile_monthlyscore60shot_json'),
    path('myprofile_quarterlyscore40shot_json/', modelFormsAppview.myprofile_quarterlyscore40shot_json, name='myprofile_quarterlyscore40shot_json'),
    path('myprofile_quarterlyscore60shot_json/', modelFormsAppview.myprofile_quarterlyscore60shot_json, name='myprofile_quarterlyscore60shot_json'),
    path('myprofile_quarterlybarrel40shot_json/', modelFormsAppview.myprofile_quarterlybarrel40shot_json, name='myprofile_quarterlybarrel40shot_json'),
    path('myprofile_quarterlybarrel60shot_json/', modelFormsAppview.myprofile_quarterlybarrel60shot_json, name='myprofile_quarterlybarrel60shot_json'),
    ##################################################################
    # Technical Graph Views
    path('technical_statistics/', modelFormsAppview.technical_statistics),

    ##################################################################
    #below one was created just to test multi axis line chart but not done yet
    path('alluser_scorechartquarterly/', modelFormsAppview.alluser_scorechartquarterly, name='alluser_scorechartquarterly'),
    path('', modelFormsAppview.landingpage),
]
