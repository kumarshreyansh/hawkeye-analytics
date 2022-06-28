from datetime import date
import imp
from pprint import pprint
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, HttpResponseRedirect
from modelFormsApp.models import ModelClass
from modelFormsApp.forms import FormClass
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.db import connection
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import statistics
from scipy.stats import linregress
# Create your views here.

# def home(request):
#     return render(request, 'modelFormsApp/home.html', {})
@login_required
@permission_required('modelFormsApp.view_modelclass')
def coach(request):
    return render(request, 'modelFormsApp/coach.html', {})
# @login_required
# @permission_required('modelFormsApp.view_modelclass')
# def listallentries(request):
#     mylist = ModelClass.objects.all()
#     return render(request, 'modelFormsApp/listallentries.html', {'mylist': mylist})
@login_required
def addnewentry(request):
    form = FormClass()
    if request.method == "POST":
        form = FormClass(request.POST)
        if form.is_valid():
            #form.save() version 1 line
            form_inst = form.save(commit=False)
            form_inst.shooterid = request.user
            form_inst.save()
        else:
            return HttpResponse('<p>Invalid data format</p>')
        #return HttpResponseRedirect("/home")
        return HttpResponseRedirect("http://127.0.0.1:8000")
    return render(request, 'modelFormsApp/addnewentry.html', {'form': form})

def logout(request):
    return render(request, 'modelFormsApp/logout.html')

# @login_required
# @permission_required('modelFormsApp.view_modelclass')
# def todaytable(request):
#     todaylist = ModelClass.objects.filter(matchDate__exact=date.today())
#     return render(request, 'modelFormsApp/todaytable.html', {'todaylist': todaylist})

@login_required
@permission_required('modelFormsApp.view_modelclass')
def todayrifle(request):
    rifle40shotlist = ModelClass.objects.filter(matchDate=date.today(), shooterid__weapontype = '1', totalshots='0')
    riflelist = ModelClass.objects.filter(matchDate=date.today(), shooterid__weapontype = '1', totalshots='1')
    return render(request, 'modelFormsApp/todayrifle.html', {'riflelist': riflelist, 'rifle40shotlist': rifle40shotlist})

@login_required
@permission_required('modelFormsApp.view_modelclass')
def todayriflewomen(request):
    riflelist40shotwomen = ModelClass.objects.filter(matchDate=date.today(), shooterid__weapontype = '1', shooterid__gender='1', totalshots='0')
    riflelistwomen = ModelClass.objects.filter(matchDate=date.today(), shooterid__weapontype = '1', shooterid__gender='1', totalshots='1')
    return render(request, 'modelFormsApp/todayriflewomen.html', {'riflelistwomen': riflelistwomen, 'riflelist40shotwomen': riflelist40shotwomen})

@login_required
@permission_required('modelFormsApp.view_modelclass')
def todayriflemen(request):
    riflelist40shotmen = ModelClass.objects.filter(matchDate=date.today(), shooterid__weapontype = '1', shooterid__gender='0', totalshots='0')
    riflelistmen = ModelClass.objects.filter(matchDate=date.today(), shooterid__weapontype = '1', shooterid__gender='0', totalshots='1')
    return render(request, 'modelFormsApp/todayriflemen.html', {'riflelistmen': riflelistmen, 'riflelist40shotmen': riflelist40shotmen})

@login_required
@permission_required('modelFormsApp.view_modelclass')
def todaypistol(request):
    pistol40shotlist = ModelClass.objects.filter(matchDate=date.today(), shooterid__weapontype = '0', totalshots='0')
    pistollist = ModelClass.objects.filter(matchDate=date.today(), shooterid__weapontype = '0', totalshots='1')
    return render(request, 'modelFormsApp/todaypistol.html', {'pistollist': pistollist, 'pistol40shotlist': pistol40shotlist})

@login_required
@permission_required('modelFormsApp.view_modelclass')
def todaypistolwomen(request):
    pistollistwomen = ModelClass.objects.filter(matchDate=date.today(), shooterid__weapontype = '0', shooterid__gender='1', totalshots='1')
    pistollist40shotwomen = ModelClass.objects.filter(matchDate=date.today(), shooterid__weapontype = '0', shooterid__gender='1', totalshots='0')
    return render(request, 'modelFormsApp/todaypistolwomen.html', {'pistollistwomen': pistollistwomen, 'pistollist40shotwomen': pistollist40shotwomen})

@login_required
@permission_required('modelFormsApp.view_modelclass')
def todaypistolmen(request):
    pistollistmen = ModelClass.objects.filter(matchDate=date.today(), shooterid__weapontype = '0', shooterid__gender='0', totalshots='1')
    pistollist40shotmen = ModelClass.objects.filter(matchDate=date.today(), shooterid__weapontype = '0', shooterid__gender='0', totalshots='0')
    return render(request, 'modelFormsApp/todaypistolmen.html', {'pistollistmen': pistollistmen, 'pistollist40shotmen': pistollist40shotmen})

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

@login_required
@permission_required('modelFormsApp.view_modelclass')
def monthlypistol(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT user_table.username, CAST(AVG(model_table.matchscore) AS DECIMAL(10,2)) AS matchscore, CAST(AVG(model_table.higheastseriesscore) AS DECIMAL(10,2)) AS higheastseriesscore, CAST(AVG(model_table.numberoftens) AS DECIMAL(10,2)) AS numberoftens, CAST(AVG(model_table.cancellationofbadshot) AS DECIMAL(10,2)) AS cancellationofbadshot, CAST(AVG(model_table.stabilityofsightpicture) AS DECIMAL(10,2)) AS stabilityofsightpicture, CAST(AVG(model_table.flowoftheshot) AS DECIMAL(10,2)) AS flowoftheshot, CAST(AVG(model_table.visualization) AS DECIMAL(10,2)) AS visualization, CAST(AVG(model_table.bodybalance) AS DECIMAL(10,2)) AS bodybalance, CAST(AVG(model_table.ninetydegreetriggeroperation) AS DECIMAL(10,2)) AS ninetydegreetriggeroperation, CAST(AVG(model_table.averageshotduration) AS DECIMAL(10,2)) AS averageshotduration, CAST(AVG(model_table.followthrough) AS DECIMAL(10,2)) AS followthrough, CAST(AVG(model_table.mentalstability) AS DECIMAL(10,2)) AS mentalstability, CAST(AVG(model_table.hydrationlevel) AS DECIMAL(10,2)) AS hydrationlevel, CAST(AVG(model_table.fueling) AS DECIMAL(10,2)) AS fueling FROM model_table, user_table WHERE user_table.id = model_table.shooterid_id AND (MONTH(matchDate) = MONTH(CURRENT_DATE()) AND YEAR(matchDate) = YEAR(CURRENT_DATE())) AND (user_table.weapontype = '0') AND model_table.totalshots = '0' GROUP BY user_table.id ORDER BY matchscore DESC;")
        monthlypistol40shotlist = dictfetchall(cursor)
    with connection.cursor() as cursor:
        cursor.execute("SELECT user_table.username, CAST(AVG(model_table.matchscore) AS DECIMAL(10,2)) AS matchscore, CAST(AVG(model_table.higheastseriesscore) AS DECIMAL(10,2)) AS higheastseriesscore, CAST(AVG(model_table.numberoftens) AS DECIMAL(10,2)) AS numberoftens, CAST(AVG(model_table.cancellationofbadshot) AS DECIMAL(10,2)) AS cancellationofbadshot, CAST(AVG(model_table.stabilityofsightpicture) AS DECIMAL(10,2)) AS stabilityofsightpicture, CAST(AVG(model_table.flowoftheshot) AS DECIMAL(10,2)) AS flowoftheshot, CAST(AVG(model_table.visualization) AS DECIMAL(10,2)) AS visualization, CAST(AVG(model_table.bodybalance) AS DECIMAL(10,2)) AS bodybalance, CAST(AVG(model_table.ninetydegreetriggeroperation) AS DECIMAL(10,2)) AS ninetydegreetriggeroperation, CAST(AVG(model_table.averageshotduration) AS DECIMAL(10,2)) AS averageshotduration, CAST(AVG(model_table.followthrough) AS DECIMAL(10,2)) AS followthrough, CAST(AVG(model_table.mentalstability) AS DECIMAL(10,2)) AS mentalstability, CAST(AVG(model_table.hydrationlevel) AS DECIMAL(10,2)) AS hydrationlevel, CAST(AVG(model_table.fueling) AS DECIMAL(10,2)) AS fueling FROM model_table, user_table WHERE user_table.id = model_table.shooterid_id AND (MONTH(matchDate) = MONTH(CURRENT_DATE()) AND YEAR(matchDate) = YEAR(CURRENT_DATE())) AND (user_table.weapontype = '0') AND model_table.totalshots = '1' GROUP BY user_table.id;")
        #SELECT * FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE (MONTH(matchDate) = MONTH(CURRENT_DATE()) AND YEAR(matchDate) = YEAR(CURRENT_DATE())) AND (user_table.weapontype = '0');
        monthlypistollist = dictfetchall(cursor)
        return render(request, 'modelFormsApp/monthlypistol.html', {'monthlypistollist': monthlypistollist, 'monthlypistol40shotlist': monthlypistol40shotlist})

@login_required
@permission_required('modelFormsApp.view_modelclass')
def monthlyrifle(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT user_table.username, CAST(AVG(model_table.matchscore) AS DECIMAL(10,2)) AS matchscore, CAST(AVG(model_table.higheastseriesscore) AS DECIMAL(10,2)) AS higheastseriesscore, CAST(AVG(model_table.numberoftens) AS DECIMAL(10,2)) AS numberoftens, CAST(AVG(model_table.cancellationofbadshot) AS DECIMAL(10,2)) AS cancellationofbadshot, CAST(AVG(model_table.stabilityofsightpicture) AS DECIMAL(10,2)) AS stabilityofsightpicture, CAST(AVG(model_table.flowoftheshot) AS DECIMAL(10,2)) AS flowoftheshot, CAST(AVG(model_table.visualization) AS DECIMAL(10,2)) AS visualization, CAST(AVG(model_table.bodybalance) AS DECIMAL(10,2)) AS bodybalance, CAST(AVG(model_table.ninetydegreetriggeroperation) AS DECIMAL(10,2)) AS ninetydegreetriggeroperation, CAST(AVG(model_table.averageshotduration) AS DECIMAL(10,2)) AS averageshotduration, CAST(AVG(model_table.followthrough) AS DECIMAL(10,2)) AS followthrough, CAST(AVG(model_table.mentalstability) AS DECIMAL(10,2)) AS mentalstability, CAST(AVG(model_table.hydrationlevel) AS DECIMAL(10,2)) AS hydrationlevel, CAST(AVG(model_table.fueling) AS DECIMAL(10,2)) AS fueling FROM model_table, user_table WHERE user_table.id = model_table.shooterid_id AND (MONTH(matchDate) = MONTH(CURRENT_DATE()) AND YEAR(matchDate) = YEAR(CURRENT_DATE())) AND (user_table.weapontype = '1') AND model_table.totalshots = '0' GROUP BY user_table.id;")
        monthlyrifle40shotlist = dictfetchall(cursor)
    with connection.cursor() as cursor:
        cursor.execute("SELECT user_table.username, CAST(AVG(model_table.matchscore) AS DECIMAL(10,2)) AS matchscore, CAST(AVG(model_table.higheastseriesscore) AS DECIMAL(10,2)) AS higheastseriesscore, CAST(AVG(model_table.numberoftens) AS DECIMAL(10,2)) AS numberoftens, CAST(AVG(model_table.cancellationofbadshot) AS DECIMAL(10,2)) AS cancellationofbadshot, CAST(AVG(model_table.stabilityofsightpicture) AS DECIMAL(10,2)) AS stabilityofsightpicture, CAST(AVG(model_table.flowoftheshot) AS DECIMAL(10,2)) AS flowoftheshot, CAST(AVG(model_table.visualization) AS DECIMAL(10,2)) AS visualization, CAST(AVG(model_table.bodybalance) AS DECIMAL(10,2)) AS bodybalance, CAST(AVG(model_table.ninetydegreetriggeroperation) AS DECIMAL(10,2)) AS ninetydegreetriggeroperation, CAST(AVG(model_table.averageshotduration) AS DECIMAL(10,2)) AS averageshotduration, CAST(AVG(model_table.followthrough) AS DECIMAL(10,2)) AS followthrough, CAST(AVG(model_table.mentalstability) AS DECIMAL(10,2)) AS mentalstability, CAST(AVG(model_table.hydrationlevel) AS DECIMAL(10,2)) AS hydrationlevel, CAST(AVG(model_table.fueling) AS DECIMAL(10,2)) AS fueling FROM model_table, user_table WHERE user_table.id = model_table.shooterid_id AND (MONTH(matchDate) = MONTH(CURRENT_DATE()) AND YEAR(matchDate) = YEAR(CURRENT_DATE())) AND (user_table.weapontype = '1') AND model_table.totalshots = '1' GROUP BY user_table.id;")
        #SELECT * FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE (MONTH(matchDate) = MONTH(CURRENT_DATE()) AND YEAR(matchDate) = YEAR(CURRENT_DATE())) AND (user_table.weapontype = '1');
        monthlyriflelist = dictfetchall(cursor)
        return render(request, 'modelFormsApp/monthlyrifle.html', {'monthlyriflelist': monthlyriflelist, 'monthlyrifle40shotlist': monthlyrifle40shotlist})



@login_required
@permission_required('modelFormsApp.view_modelclass')
def monthlypistolwomen(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT user_table.username, CAST(AVG(model_table.matchscore) AS DECIMAL(10,2)) AS matchscore, CAST(AVG(model_table.higheastseriesscore) AS DECIMAL(10,2)) AS higheastseriesscore, CAST(AVG(model_table.numberoftens) AS DECIMAL(10,2)) AS numberoftens, CAST(AVG(model_table.cancellationofbadshot) AS DECIMAL(10,2)) AS cancellationofbadshot, CAST(AVG(model_table.stabilityofsightpicture) AS DECIMAL(10,2)) AS stabilityofsightpicture, CAST(AVG(model_table.flowoftheshot) AS DECIMAL(10,2)) AS flowoftheshot, CAST(AVG(model_table.visualization) AS DECIMAL(10,2)) AS visualization, CAST(AVG(model_table.bodybalance) AS DECIMAL(10,2)) AS bodybalance, CAST(AVG(model_table.ninetydegreetriggeroperation) AS DECIMAL(10,2)) AS ninetydegreetriggeroperation, CAST(AVG(model_table.averageshotduration) AS DECIMAL(10,2)) AS averageshotduration, CAST(AVG(model_table.followthrough) AS DECIMAL(10,2)) AS followthrough, CAST(AVG(model_table.mentalstability) AS DECIMAL(10,2)) AS mentalstability, CAST(AVG(model_table.hydrationlevel) AS DECIMAL(10,2)) AS hydrationlevel, CAST(AVG(model_table.fueling) AS DECIMAL(10,2)) AS fueling FROM model_table, user_table WHERE user_table.id = model_table.shooterid_id AND (MONTH(matchDate) = MONTH(CURRENT_DATE()) AND YEAR(matchDate) = YEAR(CURRENT_DATE())) AND (user_table.weapontype = '0') AND user_table.gender = '1' AND model_table.totalshots = '0' GROUP BY user_table.id;")
        monthlypistollist40shotwomen = dictfetchall(cursor)
    with connection.cursor() as cursor:
        cursor.execute("SELECT user_table.username, CAST(AVG(model_table.matchscore) AS DECIMAL(10,2)) AS matchscore, CAST(AVG(model_table.higheastseriesscore) AS DECIMAL(10,2)) AS higheastseriesscore, CAST(AVG(model_table.numberoftens) AS DECIMAL(10,2)) AS numberoftens, CAST(AVG(model_table.cancellationofbadshot) AS DECIMAL(10,2)) AS cancellationofbadshot, CAST(AVG(model_table.stabilityofsightpicture) AS DECIMAL(10,2)) AS stabilityofsightpicture, CAST(AVG(model_table.flowoftheshot) AS DECIMAL(10,2)) AS flowoftheshot, CAST(AVG(model_table.visualization) AS DECIMAL(10,2)) AS visualization, CAST(AVG(model_table.bodybalance) AS DECIMAL(10,2)) AS bodybalance, CAST(AVG(model_table.ninetydegreetriggeroperation) AS DECIMAL(10,2)) AS ninetydegreetriggeroperation, CAST(AVG(model_table.averageshotduration) AS DECIMAL(10,2)) AS averageshotduration, CAST(AVG(model_table.followthrough) AS DECIMAL(10,2)) AS followthrough, CAST(AVG(model_table.mentalstability) AS DECIMAL(10,2)) AS mentalstability, CAST(AVG(model_table.hydrationlevel) AS DECIMAL(10,2)) AS hydrationlevel, CAST(AVG(model_table.fueling) AS DECIMAL(10,2)) AS fueling FROM model_table, user_table WHERE user_table.id = model_table.shooterid_id AND (MONTH(matchDate) = MONTH(CURRENT_DATE()) AND YEAR(matchDate) = YEAR(CURRENT_DATE())) AND (user_table.weapontype = '0') AND user_table.gender = '1' AND model_table.totalshots = '1' GROUP BY user_table.id;")
        monthlypistollistwomen = dictfetchall(cursor)
        return render(request, 'modelFormsApp/monthlypistolwomen.html', {'monthlypistollistwomen': monthlypistollistwomen, 'monthlypistollist40shotwomen': monthlypistollist40shotwomen})

@login_required
@permission_required('modelFormsApp.view_modelclass')
def monthlypistolmen(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT user_table.username, CAST(AVG(model_table.matchscore) AS DECIMAL(10,2)) AS matchscore, CAST(AVG(model_table.higheastseriesscore) AS DECIMAL(10,2)) AS higheastseriesscore, CAST(AVG(model_table.numberoftens) AS DECIMAL(10,2)) AS numberoftens, CAST(AVG(model_table.cancellationofbadshot) AS DECIMAL(10,2)) AS cancellationofbadshot, CAST(AVG(model_table.stabilityofsightpicture) AS DECIMAL(10,2)) AS stabilityofsightpicture, CAST(AVG(model_table.flowoftheshot) AS DECIMAL(10,2)) AS flowoftheshot, CAST(AVG(model_table.visualization) AS DECIMAL(10,2)) AS visualization, CAST(AVG(model_table.bodybalance) AS DECIMAL(10,2)) AS bodybalance, CAST(AVG(model_table.ninetydegreetriggeroperation) AS DECIMAL(10,2)) AS ninetydegreetriggeroperation, CAST(AVG(model_table.averageshotduration) AS DECIMAL(10,2)) AS averageshotduration, CAST(AVG(model_table.followthrough) AS DECIMAL(10,2)) AS followthrough, CAST(AVG(model_table.mentalstability) AS DECIMAL(10,2)) AS mentalstability, CAST(AVG(model_table.hydrationlevel) AS DECIMAL(10,2)) AS hydrationlevel, CAST(AVG(model_table.fueling) AS DECIMAL(10,2)) AS fueling FROM model_table, user_table WHERE user_table.id = model_table.shooterid_id AND (MONTH(matchDate) = MONTH(CURRENT_DATE()) AND YEAR(matchDate) = YEAR(CURRENT_DATE())) AND (user_table.weapontype = '0') AND user_table.gender = '0' AND model_table.totalshots = '0' GROUP BY user_table.id;")
        monthlypistollist40shotmen = dictfetchall(cursor)
    with connection.cursor() as cursor:
        cursor.execute("SELECT user_table.username, CAST(AVG(model_table.matchscore) AS DECIMAL(10,2)) AS matchscore, CAST(AVG(model_table.higheastseriesscore) AS DECIMAL(10,2)) AS higheastseriesscore, CAST(AVG(model_table.numberoftens) AS DECIMAL(10,2)) AS numberoftens, CAST(AVG(model_table.cancellationofbadshot) AS DECIMAL(10,2)) AS cancellationofbadshot, CAST(AVG(model_table.stabilityofsightpicture) AS DECIMAL(10,2)) AS stabilityofsightpicture, CAST(AVG(model_table.flowoftheshot) AS DECIMAL(10,2)) AS flowoftheshot, CAST(AVG(model_table.visualization) AS DECIMAL(10,2)) AS visualization, CAST(AVG(model_table.bodybalance) AS DECIMAL(10,2)) AS bodybalance, CAST(AVG(model_table.ninetydegreetriggeroperation) AS DECIMAL(10,2)) AS ninetydegreetriggeroperation, CAST(AVG(model_table.averageshotduration) AS DECIMAL(10,2)) AS averageshotduration, CAST(AVG(model_table.followthrough) AS DECIMAL(10,2)) AS followthrough, CAST(AVG(model_table.mentalstability) AS DECIMAL(10,2)) AS mentalstability, CAST(AVG(model_table.hydrationlevel) AS DECIMAL(10,2)) AS hydrationlevel, CAST(AVG(model_table.fueling) AS DECIMAL(10,2)) AS fueling FROM model_table, user_table WHERE user_table.id = model_table.shooterid_id AND (MONTH(matchDate) = MONTH(CURRENT_DATE()) AND YEAR(matchDate) = YEAR(CURRENT_DATE())) AND (user_table.weapontype = '0') AND user_table.gender = '0' AND model_table.totalshots = '1' GROUP BY user_table.id;")
        monthlypistollistmen = dictfetchall(cursor)
        return render(request, 'modelFormsApp/monthlypistolmen.html', {'monthlypistollistmen': monthlypistollistmen, 'monthlypistollist40shotmen': monthlypistollist40shotmen})


@login_required
@permission_required('modelFormsApp.view_modelclass')
def quarterlypistol(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT user_table.username, CAST(AVG(model_table.matchscore) AS DECIMAL(10,2)) AS matchscore, CAST(AVG(model_table.higheastseriesscore) AS DECIMAL(10,2)) AS higheastseriesscore, CAST(AVG(model_table.numberoftens) AS DECIMAL(10,2)) AS numberoftens, CAST(AVG(model_table.cancellationofbadshot) AS DECIMAL(10,2)) AS cancellationofbadshot, CAST(AVG(model_table.stabilityofsightpicture) AS DECIMAL(10,2)) AS stabilityofsightpicture, CAST(AVG(model_table.flowoftheshot) AS DECIMAL(10,2)) AS flowoftheshot, CAST(AVG(model_table.visualization) AS DECIMAL(10,2)) AS visualization, CAST(AVG(model_table.bodybalance) AS DECIMAL(10,2)) AS bodybalance, CAST(AVG(model_table.ninetydegreetriggeroperation) AS DECIMAL(10,2)) AS ninetydegreetriggeroperation, CAST(AVG(model_table.averageshotduration) AS DECIMAL(10,2)) AS averageshotduration, CAST(AVG(model_table.followthrough) AS DECIMAL(10,2)) AS followthrough, CAST(AVG(model_table.mentalstability) AS DECIMAL(10,2)) AS mentalstability, CAST(AVG(model_table.hydrationlevel) AS DECIMAL(10,2)) AS hydrationlevel, CAST(AVG(model_table.fueling) AS DECIMAL(10,2)) AS fueling FROM model_table, user_table WHERE user_table.id = model_table.shooterid_id AND (DATE_ADD(CURDATE(), INTERVAL -3 MONTH)) AND (user_table.weapontype = '0') AND model_table.totalshots = '0' GROUP BY user_table.id ORDER BY matchscore DESC;")
        quarterlypistol40shotlist = dictfetchall(cursor)
    with connection.cursor() as cursor:
        cursor.execute("SELECT user_table.username, CAST(AVG(model_table.matchscore) AS DECIMAL(10,2)) AS matchscore, CAST(AVG(model_table.higheastseriesscore) AS DECIMAL(10,2)) AS higheastseriesscore, CAST(AVG(model_table.numberoftens) AS DECIMAL(10,2)) AS numberoftens, CAST(AVG(model_table.cancellationofbadshot) AS DECIMAL(10,2)) AS cancellationofbadshot, CAST(AVG(model_table.stabilityofsightpicture) AS DECIMAL(10,2)) AS stabilityofsightpicture, CAST(AVG(model_table.flowoftheshot) AS DECIMAL(10,2)) AS flowoftheshot, CAST(AVG(model_table.visualization) AS DECIMAL(10,2)) AS visualization, CAST(AVG(model_table.bodybalance) AS DECIMAL(10,2)) AS bodybalance, CAST(AVG(model_table.ninetydegreetriggeroperation) AS DECIMAL(10,2)) AS ninetydegreetriggeroperation, CAST(AVG(model_table.averageshotduration) AS DECIMAL(10,2)) AS averageshotduration, CAST(AVG(model_table.followthrough) AS DECIMAL(10,2)) AS followthrough, CAST(AVG(model_table.mentalstability) AS DECIMAL(10,2)) AS mentalstability, CAST(AVG(model_table.hydrationlevel) AS DECIMAL(10,2)) AS hydrationlevel, CAST(AVG(model_table.fueling) AS DECIMAL(10,2)) AS fueling FROM model_table, user_table WHERE user_table.id = model_table.shooterid_id AND (DATE_ADD(CURDATE(), INTERVAL -3 MONTH)) AND (user_table.weapontype = '0') AND model_table.totalshots = '1' GROUP BY user_table.id ORDER BY matchscore DESC;")
        #SELECT user_table.username, AVG(model_table.matchscore) AS matchscore, AVG(model_table.flowoftheshot) AS flowoftheshot, AVG(model_table.visualization) AS visualization, AVG(model_table.bodybalance) AS bodybalance, AVG(model_table.ninetydegreetriggeroperation) AS ninetydegreetriggeroperation, AVG(model_table.averageshotduration) AS averageshotduration, AVG(model_table.followthrough) AS followthrough, AVG(model_table.mentalstability) AS mentalstability FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE (DATE_ADD(CURDATE(), INTERVAL -3 MONTH)) AND (user_table.weapontype = '0') GROUP BY user_table.id;

        quarterlypistollist = dictfetchall(cursor)
        # p = Paginator(quarterlypistollistdata, 2)
        # page_number = request.GET.get('page')
        # try:
        #     quarterlypistollist = p.get_page(page_number)
        # except PageNotAnInteger:
        #     quarterlypistollist = p.page(1)
        # except EmptyPage:
        #     quarterlypistollist = p.page(p.num_pages)

        return render(request, 'modelFormsApp/quarterlypistol.html', {'quarterlypistollist': quarterlypistollist, 'quarterlypistol40shotlist': quarterlypistol40shotlist})

@login_required
@permission_required('modelFormsApp.view_modelclass')
def quarterlyrifle(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT user_table.username, CAST(AVG(model_table.matchscore) AS DECIMAL(10,2)) AS matchscore, CAST(AVG(model_table.higheastseriesscore) AS DECIMAL(10,2)) AS higheastseriesscore, CAST(AVG(model_table.numberoftens) AS DECIMAL(10,2)) AS numberoftens, CAST(AVG(model_table.cancellationofbadshot) AS DECIMAL(10,2)) AS cancellationofbadshot, CAST(AVG(model_table.stabilityofsightpicture) AS DECIMAL(10,2)) AS stabilityofsightpicture, CAST(AVG(model_table.flowoftheshot) AS DECIMAL(10,2)) AS flowoftheshot, CAST(AVG(model_table.visualization) AS DECIMAL(10,2)) AS visualization, CAST(AVG(model_table.bodybalance) AS DECIMAL(10,2)) AS bodybalance, CAST(AVG(model_table.ninetydegreetriggeroperation) AS DECIMAL(10,2)) AS ninetydegreetriggeroperation, CAST(AVG(model_table.averageshotduration) AS DECIMAL(10,2)) AS averageshotduration, CAST(AVG(model_table.followthrough) AS DECIMAL(10,2)) AS followthrough, CAST(AVG(model_table.mentalstability) AS DECIMAL(10,2)) AS mentalstability, CAST(AVG(model_table.hydrationlevel) AS DECIMAL(10,2)) AS hydrationlevel, CAST(AVG(model_table.fueling) AS DECIMAL(10,2)) AS fueling FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE (DATE_ADD(CURDATE(), INTERVAL -3 MONTH)) AND (user_table.weapontype = '1') AND model_table.totalshots = '0' GROUP BY user_table.id;")
        quarterlyrfile40shotlist = dictfetchall(cursor)
    with connection.cursor() as cursor:
        cursor.execute("SELECT user_table.username, CAST(AVG(model_table.matchscore) AS DECIMAL(10,2)) AS matchscore, CAST(AVG(model_table.higheastseriesscore) AS DECIMAL(10,2)) AS higheastseriesscore, CAST(AVG(model_table.numberoftens) AS DECIMAL(10,2)) AS numberoftens, CAST(AVG(model_table.cancellationofbadshot) AS DECIMAL(10,2)) AS cancellationofbadshot, CAST(AVG(model_table.stabilityofsightpicture) AS DECIMAL(10,2)) AS stabilityofsightpicture, CAST(AVG(model_table.flowoftheshot) AS DECIMAL(10,2)) AS flowoftheshot, CAST(AVG(model_table.visualization) AS DECIMAL(10,2)) AS visualization, CAST(AVG(model_table.bodybalance) AS DECIMAL(10,2)) AS bodybalance, CAST(AVG(model_table.ninetydegreetriggeroperation) AS DECIMAL(10,2)) AS ninetydegreetriggeroperation, CAST(AVG(model_table.averageshotduration) AS DECIMAL(10,2)) AS averageshotduration, CAST(AVG(model_table.followthrough) AS DECIMAL(10,2)) AS followthrough, CAST(AVG(model_table.mentalstability) AS DECIMAL(10,2)) AS mentalstability, CAST(AVG(model_table.hydrationlevel) AS DECIMAL(10,2)) AS hydrationlevel, CAST(AVG(model_table.fueling) AS DECIMAL(10,2)) AS fueling FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE (DATE_ADD(CURDATE(), INTERVAL -3 MONTH)) AND (user_table.weapontype = '1') AND model_table.totalshots = '1' GROUP BY user_table.id;")
        quarterlyrfilelist = dictfetchall(cursor)
        return render(request, 'modelFormsApp/quarterlyrifle.html', {'quarterlyrfilelist': quarterlyrfilelist, 'quarterlyrfile40shotlist': quarterlyrfile40shotlist})

@login_required
@permission_required('modelFormsApp.view_modelclass')
def quarterlypistolwomen(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT user_table.username, CAST(AVG(model_table.matchscore) AS DECIMAL(10,2)) AS matchscore, CAST(AVG(model_table.higheastseriesscore) AS DECIMAL(10,2)) AS higheastseriesscore, CAST(AVG(model_table.numberoftens) AS DECIMAL(10,2)) AS numberoftens, CAST(AVG(model_table.cancellationofbadshot) AS DECIMAL(10,2)) AS cancellationofbadshot, CAST(AVG(model_table.stabilityofsightpicture) AS DECIMAL(10,2)) AS stabilityofsightpicture, CAST(AVG(model_table.flowoftheshot) AS DECIMAL(10,2)) AS flowoftheshot, CAST(AVG(model_table.visualization) AS DECIMAL(10,2)) AS visualization, CAST(AVG(model_table.bodybalance) AS DECIMAL(10,2)) AS bodybalance, CAST(AVG(model_table.ninetydegreetriggeroperation) AS DECIMAL(10,2)) AS ninetydegreetriggeroperation, CAST(AVG(model_table.averageshotduration) AS DECIMAL(10,2)) AS averageshotduration, CAST(AVG(model_table.followthrough) AS DECIMAL(10,2)) AS followthrough, CAST(AVG(model_table.mentalstability) AS DECIMAL(10,2)) AS mentalstability, CAST(AVG(model_table.hydrationlevel) AS DECIMAL(10,2)) AS hydrationlevel, CAST(AVG(model_table.fueling) AS DECIMAL(10,2)) AS fueling FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE (DATE_ADD(CURDATE(), INTERVAL -3 MONTH)) AND (user_table.gender = '1' AND user_table.weapontype = '0') AND model_table.totalshots = '0' GROUP BY user_table.id;")
        quarterlypistollist40shotwomen = dictfetchall(cursor)
    with connection.cursor() as cursor:
        cursor.execute("SELECT user_table.username, CAST(AVG(model_table.matchscore) AS DECIMAL(10,2)) AS matchscore, CAST(AVG(model_table.higheastseriesscore) AS DECIMAL(10,2)) AS higheastseriesscore, CAST(AVG(model_table.numberoftens) AS DECIMAL(10,2)) AS numberoftens, CAST(AVG(model_table.cancellationofbadshot) AS DECIMAL(10,2)) AS cancellationofbadshot, CAST(AVG(model_table.stabilityofsightpicture) AS DECIMAL(10,2)) AS stabilityofsightpicture, CAST(AVG(model_table.flowoftheshot) AS DECIMAL(10,2)) AS flowoftheshot, CAST(AVG(model_table.visualization) AS DECIMAL(10,2)) AS visualization, CAST(AVG(model_table.bodybalance) AS DECIMAL(10,2)) AS bodybalance, CAST(AVG(model_table.ninetydegreetriggeroperation) AS DECIMAL(10,2)) AS ninetydegreetriggeroperation, CAST(AVG(model_table.averageshotduration) AS DECIMAL(10,2)) AS averageshotduration, CAST(AVG(model_table.followthrough) AS DECIMAL(10,2)) AS followthrough, CAST(AVG(model_table.mentalstability) AS DECIMAL(10,2)) AS mentalstability, CAST(AVG(model_table.hydrationlevel) AS DECIMAL(10,2)) AS hydrationlevel, CAST(AVG(model_table.fueling) AS DECIMAL(10,2)) AS fueling FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE (DATE_ADD(CURDATE(), INTERVAL -3 MONTH)) AND (user_table.gender = '1' AND user_table.weapontype = '0') AND model_table.totalshots = '1' GROUP BY user_table.id;")
        quarterlypistollistwomen = dictfetchall(cursor)
        return render(request, 'modelFormsApp/quarterlypistolwomen.html', {'quarterlypistollistwomen': quarterlypistollistwomen, 'quarterlypistollist40shotwomen': quarterlypistollist40shotwomen})


@login_required
@permission_required('modelFormsApp.view_modelclass')
def quarterlypistolmen(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT user_table.username, CAST(AVG(model_table.matchscore) AS DECIMAL(10,2)) AS matchscore, CAST(AVG(model_table.higheastseriesscore) AS DECIMAL(10,2)) AS higheastseriesscore, CAST(AVG(model_table.numberoftens) AS DECIMAL(10,2)) AS numberoftens, CAST(AVG(model_table.cancellationofbadshot) AS DECIMAL(10,2)) AS cancellationofbadshot, CAST(AVG(model_table.stabilityofsightpicture) AS DECIMAL(10,2)) AS stabilityofsightpicture, CAST(AVG(model_table.flowoftheshot) AS DECIMAL(10,2)) AS flowoftheshot, CAST(AVG(model_table.visualization) AS DECIMAL(10,2)) AS visualization, CAST(AVG(model_table.bodybalance) AS DECIMAL(10,2)) AS bodybalance, CAST(AVG(model_table.ninetydegreetriggeroperation) AS DECIMAL(10,2)) AS ninetydegreetriggeroperation, CAST(AVG(model_table.averageshotduration) AS DECIMAL(10,2)) AS averageshotduration, CAST(AVG(model_table.followthrough) AS DECIMAL(10,2)) AS followthrough, CAST(AVG(model_table.mentalstability) AS DECIMAL(10,2)) AS mentalstability, CAST(AVG(model_table.hydrationlevel) AS DECIMAL(10,2)) AS hydrationlevel, CAST(AVG(model_table.fueling) AS DECIMAL(10,2)) AS fueling FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE (DATE_ADD(CURDATE(), INTERVAL -3 MONTH)) AND (user_table.gender = '0' AND user_table.weapontype = '0') AND model_table.totalshots = '0' GROUP BY user_table.id ORDER BY matchscore DESC;")
        quarterlypistollist40shotmen = dictfetchall(cursor)
    with connection.cursor() as cursor:
        cursor.execute("SELECT user_table.username, CAST(AVG(model_table.matchscore) AS DECIMAL(10,2)) AS matchscore, CAST(AVG(model_table.higheastseriesscore) AS DECIMAL(10,2)) AS higheastseriesscore, CAST(AVG(model_table.numberoftens) AS DECIMAL(10,2)) AS numberoftens, CAST(AVG(model_table.cancellationofbadshot) AS DECIMAL(10,2)) AS cancellationofbadshot, CAST(AVG(model_table.stabilityofsightpicture) AS DECIMAL(10,2)) AS stabilityofsightpicture, CAST(AVG(model_table.flowoftheshot) AS DECIMAL(10,2)) AS flowoftheshot, CAST(AVG(model_table.visualization) AS DECIMAL(10,2)) AS visualization, CAST(AVG(model_table.bodybalance) AS DECIMAL(10,2)) AS bodybalance, CAST(AVG(model_table.ninetydegreetriggeroperation) AS DECIMAL(10,2)) AS ninetydegreetriggeroperation, CAST(AVG(model_table.averageshotduration) AS DECIMAL(10,2)) AS averageshotduration, CAST(AVG(model_table.followthrough) AS DECIMAL(10,2)) AS followthrough, CAST(AVG(model_table.mentalstability) AS DECIMAL(10,2)) AS mentalstability, CAST(AVG(model_table.hydrationlevel) AS DECIMAL(10,2)) AS hydrationlevel, CAST(AVG(model_table.fueling) AS DECIMAL(10,2)) AS fueling FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE (DATE_ADD(CURDATE(), INTERVAL -3 MONTH)) AND (user_table.gender = '0' AND user_table.weapontype = '0') AND model_table.totalshots = '1' GROUP BY user_table.id ORDER BY matchscore DESC;")
        quarterlypistollistmen = dictfetchall(cursor)
        return render(request, 'modelFormsApp/quarterlypistolmen.html', {'quarterlypistollistmen': quarterlypistollistmen, 'quarterlypistollist40shotmen': quarterlypistollist40shotmen})

@login_required
@permission_required('modelFormsApp.view_modelclass')
def quarterlyriflewomen(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT user_table.username, CAST(AVG(model_table.matchscore) AS DECIMAL(10,2)) AS matchscore, CAST(AVG(model_table.higheastseriesscore) AS DECIMAL(10,2)) AS higheastseriesscore, CAST(AVG(model_table.numberoftens) AS DECIMAL(10,2)) AS numberoftens, CAST(AVG(model_table.cancellationofbadshot) AS DECIMAL(10,2)) AS cancellationofbadshot, CAST(AVG(model_table.stabilityofsightpicture) AS DECIMAL(10,2)) AS stabilityofsightpicture, CAST(AVG(model_table.flowoftheshot) AS DECIMAL(10,2)) AS flowoftheshot, CAST(AVG(model_table.visualization) AS DECIMAL(10,2)) AS visualization, CAST(AVG(model_table.bodybalance) AS DECIMAL(10,2)) AS bodybalance, CAST(AVG(model_table.ninetydegreetriggeroperation) AS DECIMAL(10,2)) AS ninetydegreetriggeroperation, CAST(AVG(model_table.averageshotduration) AS DECIMAL(10,2)) AS averageshotduration, CAST(AVG(model_table.followthrough) AS DECIMAL(10,2)) AS followthrough, CAST(AVG(model_table.mentalstability) AS DECIMAL(10,2)) AS mentalstability, CAST(AVG(model_table.hydrationlevel) AS DECIMAL(10,2)) AS hydrationlevel, CAST(AVG(model_table.fueling) AS DECIMAL(10,2)) AS fueling FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE (DATE_ADD(CURDATE(), INTERVAL -3 MONTH)) AND (user_table.gender = '1' AND user_table.weapontype = '1') AND model_table.totalshots = '0' GROUP BY user_table.id;")
        quarterlyriflelist40shotwomen = dictfetchall(cursor)
    with connection.cursor() as cursor:
        cursor.execute("SELECT user_table.username, CAST(AVG(model_table.matchscore) AS DECIMAL(10,2)) AS matchscore, CAST(AVG(model_table.higheastseriesscore) AS DECIMAL(10,2)) AS higheastseriesscore, CAST(AVG(model_table.numberoftens) AS DECIMAL(10,2)) AS numberoftens, CAST(AVG(model_table.cancellationofbadshot) AS DECIMAL(10,2)) AS cancellationofbadshot, CAST(AVG(model_table.stabilityofsightpicture) AS DECIMAL(10,2)) AS stabilityofsightpicture, CAST(AVG(model_table.flowoftheshot) AS DECIMAL(10,2)) AS flowoftheshot, CAST(AVG(model_table.visualization) AS DECIMAL(10,2)) AS visualization, CAST(AVG(model_table.bodybalance) AS DECIMAL(10,2)) AS bodybalance, CAST(AVG(model_table.ninetydegreetriggeroperation) AS DECIMAL(10,2)) AS ninetydegreetriggeroperation, CAST(AVG(model_table.averageshotduration) AS DECIMAL(10,2)) AS averageshotduration, CAST(AVG(model_table.followthrough) AS DECIMAL(10,2)) AS followthrough, CAST(AVG(model_table.mentalstability) AS DECIMAL(10,2)) AS mentalstability, CAST(AVG(model_table.hydrationlevel) AS DECIMAL(10,2)) AS hydrationlevel, CAST(AVG(model_table.fueling) AS DECIMAL(10,2)) AS fueling FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE (DATE_ADD(CURDATE(), INTERVAL -3 MONTH)) AND (user_table.gender = '1' AND user_table.weapontype = '1') AND model_table.totalshots = '1' GROUP BY user_table.id;")
        quarterlyriflelistwomen = dictfetchall(cursor)
        return render(request, 'modelFormsApp/quarterlyriflewomen.html', {'quarterlyriflelistwomen': quarterlyriflelistwomen, 'quarterlyriflelist40shotwomen': quarterlyriflelist40shotwomen})

@login_required
@permission_required('modelFormsApp.view_modelclass')
def quarterlyriflemen(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT user_table.username, CAST(AVG(model_table.matchscore) AS DECIMAL(10,2)) AS matchscore, CAST(AVG(model_table.higheastseriesscore) AS DECIMAL(10,2)) AS higheastseriesscore, CAST(AVG(model_table.numberoftens) AS DECIMAL(10,2)) AS numberoftens, CAST(AVG(model_table.cancellationofbadshot) AS DECIMAL(10,2)) AS cancellationofbadshot, CAST(AVG(model_table.stabilityofsightpicture) AS DECIMAL(10,2)) AS stabilityofsightpicture, CAST(AVG(model_table.flowoftheshot) AS DECIMAL(10,2)) AS flowoftheshot, CAST(AVG(model_table.visualization) AS DECIMAL(10,2)) AS visualization, CAST(AVG(model_table.bodybalance) AS DECIMAL(10,2)) AS bodybalance, CAST(AVG(model_table.ninetydegreetriggeroperation) AS DECIMAL(10,2)) AS ninetydegreetriggeroperation, CAST(AVG(model_table.averageshotduration) AS DECIMAL(10,2)) AS averageshotduration, CAST(AVG(model_table.followthrough) AS DECIMAL(10,2)) AS followthrough, CAST(AVG(model_table.mentalstability) AS DECIMAL(10,2)) AS mentalstability, CAST(AVG(model_table.hydrationlevel) AS DECIMAL(10,2)) AS hydrationlevel, CAST(AVG(model_table.fueling) AS DECIMAL(10,2)) AS fueling FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE (DATE_ADD(CURDATE(), INTERVAL -3 MONTH)) AND (user_table.gender = '0' AND user_table.weapontype = '1') AND model_table.totalshots = '0' GROUP BY user_table.id;")
        quarterlyriflelist40shotmen = dictfetchall(cursor)
    with connection.cursor() as cursor:
        cursor.execute("SELECT user_table.username, CAST(AVG(model_table.matchscore) AS DECIMAL(10,2)) AS matchscore, CAST(AVG(model_table.higheastseriesscore) AS DECIMAL(10,2)) AS higheastseriesscore, CAST(AVG(model_table.numberoftens) AS DECIMAL(10,2)) AS numberoftens, CAST(AVG(model_table.cancellationofbadshot) AS DECIMAL(10,2)) AS cancellationofbadshot, CAST(AVG(model_table.stabilityofsightpicture) AS DECIMAL(10,2)) AS stabilityofsightpicture, CAST(AVG(model_table.flowoftheshot) AS DECIMAL(10,2)) AS flowoftheshot, CAST(AVG(model_table.visualization) AS DECIMAL(10,2)) AS visualization, CAST(AVG(model_table.bodybalance) AS DECIMAL(10,2)) AS bodybalance, CAST(AVG(model_table.ninetydegreetriggeroperation) AS DECIMAL(10,2)) AS ninetydegreetriggeroperation, CAST(AVG(model_table.averageshotduration) AS DECIMAL(10,2)) AS averageshotduration, CAST(AVG(model_table.followthrough) AS DECIMAL(10,2)) AS followthrough, CAST(AVG(model_table.mentalstability) AS DECIMAL(10,2)) AS mentalstability, CAST(AVG(model_table.hydrationlevel) AS DECIMAL(10,2)) AS hydrationlevel, CAST(AVG(model_table.fueling) AS DECIMAL(10,2)) AS fueling FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE (DATE_ADD(CURDATE(), INTERVAL -3 MONTH)) AND (user_table.gender = '0' AND user_table.weapontype = '1') AND model_table.totalshots = '1' GROUP BY user_table.id;")
        quarterlyriflelistmen = dictfetchall(cursor)
        return render(request, 'modelFormsApp/quarterlyriflemen.html', {'quarterlyriflelistmen': quarterlyriflelistmen, 'quarterlyriflelist40shotmen': quarterlyriflelist40shotmen})

@login_required
@permission_required('modelFormsApp.view_modelclass')
def monthlyriflewomen(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT user_table.username, CAST(AVG(model_table.matchscore) AS DECIMAL(10,2)) AS matchscore, CAST(AVG(model_table.higheastseriesscore) AS DECIMAL(10,2)) AS higheastseriesscore, CAST(AVG(model_table.numberoftens) AS DECIMAL(10,2)) AS numberoftens, CAST(AVG(model_table.cancellationofbadshot) AS DECIMAL(10,2)) AS cancellationofbadshot, CAST(AVG(model_table.stabilityofsightpicture) AS DECIMAL(10,2)) AS stabilityofsightpicture, CAST(AVG(model_table.flowoftheshot) AS DECIMAL(10,2)) AS flowoftheshot, CAST(AVG(model_table.visualization) AS DECIMAL(10,2)) AS visualization, CAST(AVG(model_table.bodybalance) AS DECIMAL(10,2)) AS bodybalance, CAST(AVG(model_table.ninetydegreetriggeroperation) AS DECIMAL(10,2)) AS ninetydegreetriggeroperation, CAST(AVG(model_table.averageshotduration) AS DECIMAL(10,2)) AS averageshotduration, CAST(AVG(model_table.followthrough) AS DECIMAL(10,2)) AS followthrough, CAST(AVG(model_table.mentalstability) AS DECIMAL(10,2)) AS mentalstability, CAST(AVG(model_table.hydrationlevel) AS DECIMAL(10,2)) AS hydrationlevel, CAST(AVG(model_table.fueling) AS DECIMAL(10,2)) AS fueling FROM model_table, user_table WHERE user_table.id = model_table.shooterid_id AND (MONTH(matchDate) = MONTH(CURRENT_DATE()) AND YEAR(matchDate) = YEAR(CURRENT_DATE())) AND (user_table.weapontype = '1') AND user_table.gender = '1' AND model_table.totalshots = '0' GROUP BY user_table.id;")
        monthlyriflelist40shotwomen = dictfetchall(cursor)
    with connection.cursor() as cursor:
        cursor.execute("SELECT user_table.username, CAST(AVG(model_table.matchscore) AS DECIMAL(10,2)) AS matchscore, CAST(AVG(model_table.higheastseriesscore) AS DECIMAL(10,2)) AS higheastseriesscore, CAST(AVG(model_table.numberoftens) AS DECIMAL(10,2)) AS numberoftens, CAST(AVG(model_table.cancellationofbadshot) AS DECIMAL(10,2)) AS cancellationofbadshot, CAST(AVG(model_table.stabilityofsightpicture) AS DECIMAL(10,2)) AS stabilityofsightpicture, CAST(AVG(model_table.flowoftheshot) AS DECIMAL(10,2)) AS flowoftheshot, CAST(AVG(model_table.visualization) AS DECIMAL(10,2)) AS visualization, CAST(AVG(model_table.bodybalance) AS DECIMAL(10,2)) AS bodybalance, CAST(AVG(model_table.ninetydegreetriggeroperation) AS DECIMAL(10,2)) AS ninetydegreetriggeroperation, CAST(AVG(model_table.averageshotduration) AS DECIMAL(10,2)) AS averageshotduration, CAST(AVG(model_table.followthrough) AS DECIMAL(10,2)) AS followthrough, CAST(AVG(model_table.mentalstability) AS DECIMAL(10,2)) AS mentalstability, CAST(AVG(model_table.hydrationlevel) AS DECIMAL(10,2)) AS hydrationlevel, CAST(AVG(model_table.fueling) AS DECIMAL(10,2)) AS fueling FROM model_table, user_table WHERE user_table.id = model_table.shooterid_id AND (MONTH(matchDate) = MONTH(CURRENT_DATE()) AND YEAR(matchDate) = YEAR(CURRENT_DATE())) AND (user_table.weapontype = '1') AND user_table.gender = '1' AND model_table.totalshots = '1' GROUP BY user_table.id;")
        monthlyriflelistwomen = dictfetchall(cursor)
        return render(request, 'modelFormsApp/monthlyriflewomen.html', {'monthlyriflelistwomen': monthlyriflelistwomen, 'monthlyriflelist40shotwomen': monthlyriflelist40shotwomen})

@login_required
@permission_required('modelFormsApp.view_modelclass')
def monthlyriflemen(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT user_table.username, CAST(AVG(model_table.matchscore) AS DECIMAL(10,2)) AS matchscore, CAST(AVG(model_table.higheastseriesscore) AS DECIMAL(10,2)) AS higheastseriesscore, CAST(AVG(model_table.numberoftens) AS DECIMAL(10,2)) AS numberoftens, CAST(AVG(model_table.cancellationofbadshot) AS DECIMAL(10,2)) AS cancellationofbadshot, CAST(AVG(model_table.stabilityofsightpicture) AS DECIMAL(10,2)) AS stabilityofsightpicture, CAST(AVG(model_table.flowoftheshot) AS DECIMAL(10,2)) AS flowoftheshot, CAST(AVG(model_table.visualization) AS DECIMAL(10,2)) AS visualization, CAST(AVG(model_table.bodybalance) AS DECIMAL(10,2)) AS bodybalance, CAST(AVG(model_table.ninetydegreetriggeroperation) AS DECIMAL(10,2)) AS ninetydegreetriggeroperation, CAST(AVG(model_table.averageshotduration) AS DECIMAL(10,2)) AS averageshotduration, CAST(AVG(model_table.followthrough) AS DECIMAL(10,2)) AS followthrough, CAST(AVG(model_table.mentalstability) AS DECIMAL(10,2)) AS mentalstability, CAST(AVG(model_table.hydrationlevel) AS DECIMAL(10,2)) AS hydrationlevel, CAST(AVG(model_table.fueling) AS DECIMAL(10,2)) AS fueling FROM model_table, user_table WHERE user_table.id = model_table.shooterid_id AND (MONTH(matchDate) = MONTH(CURRENT_DATE()) AND YEAR(matchDate) = YEAR(CURRENT_DATE())) AND (user_table.weapontype = '1') AND user_table.gender = '0' AND model_table.totalshots = '0' GROUP BY user_table.id;")
        monthlyriflelist40shotmen = dictfetchall(cursor)
    with connection.cursor() as cursor:
        cursor.execute("SELECT user_table.username, CAST(AVG(model_table.matchscore) AS DECIMAL(10,2)) AS matchscore, CAST(AVG(model_table.higheastseriesscore) AS DECIMAL(10,2)) AS higheastseriesscore, CAST(AVG(model_table.numberoftens) AS DECIMAL(10,2)) AS numberoftens, CAST(AVG(model_table.cancellationofbadshot) AS DECIMAL(10,2)) AS cancellationofbadshot, CAST(AVG(model_table.stabilityofsightpicture) AS DECIMAL(10,2)) AS stabilityofsightpicture, CAST(AVG(model_table.flowoftheshot) AS DECIMAL(10,2)) AS flowoftheshot, CAST(AVG(model_table.visualization) AS DECIMAL(10,2)) AS visualization, CAST(AVG(model_table.bodybalance) AS DECIMAL(10,2)) AS bodybalance, CAST(AVG(model_table.ninetydegreetriggeroperation) AS DECIMAL(10,2)) AS ninetydegreetriggeroperation, CAST(AVG(model_table.averageshotduration) AS DECIMAL(10,2)) AS averageshotduration, CAST(AVG(model_table.followthrough) AS DECIMAL(10,2)) AS followthrough, CAST(AVG(model_table.mentalstability) AS DECIMAL(10,2)) AS mentalstability, CAST(AVG(model_table.hydrationlevel) AS DECIMAL(10,2)) AS hydrationlevel, CAST(AVG(model_table.fueling) AS DECIMAL(10,2)) AS fueling FROM model_table, user_table WHERE user_table.id = model_table.shooterid_id AND (MONTH(matchDate) = MONTH(CURRENT_DATE()) AND YEAR(matchDate) = YEAR(CURRENT_DATE())) AND (user_table.weapontype = '1') AND user_table.gender = '0' AND model_table.totalshots = '1' GROUP BY user_table.id;")
        monthlyriflelistmen = dictfetchall(cursor)
        return render(request, 'modelFormsApp/monthlyriflemen.html', {'monthlyriflelistmen': monthlyriflelistmen, 'monthlyriflelist40shotmen': monthlyriflelist40shotmen})

@login_required
def myprofile(request):
    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT * FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE (MONTH(matchDate) = MONTH(CURRENT_DATE()) AND YEAR(matchDate) = YEAR(CURRENT_DATE())) AND user_table.username = %s ORDER BY matchdate DESC",[request.user])
        
    #     monthlylistauthuser = dictfetchall(cursor)
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE matchDate BETWEEN DATE_SUB(CURDATE(),INTERVAL 1 WEEK) AND CURDATE() AND user_table.username = %s ORDER BY matchdate DESC",[request.user])
        
        profilequarteruserlist = dictfetchall(cursor)
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE matchdate = CURRENT_DATE() AND user_table.username = %s",[request.user])
        dailylist = dictfetchall(cursor)
        return render(request, 'modelFormsApp/myprofile.html', {'profilequarteruserlist': profilequarteruserlist, 'dailylist': dailylist})

@login_required
@permission_required('modelFormsApp.view_modelclass')
def profilesuser(request, username):
#def profiles(request, *args, **kwargs):
    #username = kwargs['username']
    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT * FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE (MONTH(matchDate) = MONTH(CURRENT_DATE()) AND YEAR(matchDate) = YEAR(CURRENT_DATE())) AND user_table.username = %s ORDER BY matchDate DESC",[username])
    #     profileuserlist = dictfetchall(cursor)
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE matchDate BETWEEN DATE_SUB(CURDATE(),INTERVAL 1 WEEK) AND CURDATE() AND user_table.username = %s ORDER BY matchDate DESC",[username])
        profilequarteruserlist = dictfetchall(cursor)
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE matchdate = CURRENT_DATE() AND user_table.username = %s",[username])
        dailylist = dictfetchall(cursor)
        return render(request, 'modelFormsApp/profilesuser.html', {'profilequarteruserlist': profilequarteruserlist, 'username': username, 'dailylist': dailylist})
@login_required
@permission_required('modelFormsApp.view_modelclass')
def profilesuser40shot_json(request, username):
    labels = []
    data = []
    username = username

    with connection.cursor() as cursor:
        cursor.execute("SELECT model_table.matchDate, model_table.matchscore FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE (MONTH(matchDate) = MONTH(CURRENT_DATE()) AND YEAR(matchDate) = YEAR(CURRENT_DATE())) AND model_table.totalshots = '0' AND user_table.username = %s ORDER BY matchDate",[username])

        queryset = dictfetchall(cursor)
        print(queryset)
        for each in queryset:
            print(each['matchDate'])
            print(each['matchscore'])
            labels.append(each['matchDate'])
            data.append(each['matchscore'])
        
        return JsonResponse(data={
            'labels': labels,
            'data': data,
        })

@login_required
@permission_required('modelFormsApp.view_modelclass')
def profilesuser60shot_json(request, username):
    labels = []
    data = []
    username = username

    with connection.cursor() as cursor:
        cursor.execute("SELECT model_table.matchDate, model_table.matchscore FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE (MONTH(matchDate) = MONTH(CURRENT_DATE()) AND YEAR(matchDate) = YEAR(CURRENT_DATE())) AND model_table.totalshots = '1' AND user_table.username = %s ORDER BY matchDate",[username])

        queryset = dictfetchall(cursor)
        print(queryset)
        for each in queryset:
            print(each['matchDate'])
            print(each['matchscore'])
            labels.append(each['matchDate'])
            data.append(each['matchscore'])
        
        return JsonResponse(data={
            'labels': labels,
            'data': data,
        })


@login_required
@permission_required('modelFormsApp.view_modelclass')
def profilesuserhigheastseriesscore40shot_json(request, username):
    labels = []
    data = []
    username = username

    with connection.cursor() as cursor:
        cursor.execute("SELECT model_table.matchDate, model_table.higheastseriesscore FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE (MONTH(matchDate) = MONTH(CURRENT_DATE()) AND YEAR(matchDate) = YEAR(CURRENT_DATE())) AND model_table.totalshots = '0' AND user_table.username = %s ORDER BY matchDate",[username])

        queryset = dictfetchall(cursor)
        print(queryset)
        for each in queryset:
            print(each['matchDate'])
            print(each['higheastseriesscore'])
            labels.append(each['matchDate'])
            data.append(each['higheastseriesscore'])
        
        return JsonResponse(data={
            'labels': labels,
            'data': data,
        })

@login_required
@permission_required('modelFormsApp.view_modelclass')
def profilesuserhigheastseriesscore60shot_json(request, username):
    labels = []
    data = []
    username = username

    with connection.cursor() as cursor:
        cursor.execute("SELECT model_table.matchDate, model_table.higheastseriesscore FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE (MONTH(matchDate) = MONTH(CURRENT_DATE()) AND YEAR(matchDate) = YEAR(CURRENT_DATE())) AND model_table.totalshots = '1' AND user_table.username = %s ORDER BY matchDate",[username])

        queryset = dictfetchall(cursor)
        print(queryset)
        for each in queryset:
            print(each['matchDate'])
            print(each['higheastseriesscore'])
            labels.append(each['matchDate'])
            data.append(each['higheastseriesscore'])
        
        return JsonResponse(data={
            'labels': labels,
            'data': data,
        })

@login_required
@permission_required('modelFormsApp.view_modelclass')
def profilesusernumberoftens40shot_json(request, username):
    labels = []
    data = []
    username = username

    with connection.cursor() as cursor:
        cursor.execute("SELECT model_table.matchDate, model_table.numberoftens FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE (MONTH(matchDate) = MONTH(CURRENT_DATE()) AND YEAR(matchDate) = YEAR(CURRENT_DATE())) AND model_table.totalshots = '0' AND user_table.username = %s ORDER BY matchDate",[username])

        queryset = dictfetchall(cursor)
        print(queryset)
        for each in queryset:
            print(each['matchDate'])
            print(each['numberoftens'])
            labels.append(each['matchDate'])
            data.append(each['numberoftens'])
        
        return JsonResponse(data={
            'labels': labels,
            'data': data,
        })

@login_required
@permission_required('modelFormsApp.view_modelclass')
def profilesusernumberoftens60shot_json(request, username):
    labels = []
    data = []
    username = username

    with connection.cursor() as cursor:
        cursor.execute("SELECT model_table.matchDate, model_table.numberoftens FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE (MONTH(matchDate) = MONTH(CURRENT_DATE()) AND YEAR(matchDate) = YEAR(CURRENT_DATE())) AND model_table.totalshots = '1' AND user_table.username = %s ORDER BY matchDate",[username])

        queryset = dictfetchall(cursor)
        print(queryset)
        for each in queryset:
            print(each['matchDate'])
            print(each['numberoftens'])
            labels.append(each['matchDate'])
            data.append(each['numberoftens'])
        
        return JsonResponse(data={
            'labels': labels,
            'data': data,
        })

@login_required
@permission_required('modelFormsApp.view_modelclass')
def profilesusercancellationofbadshot40shot_json(request, username):
    labels = []
    data = []
    username = username

    with connection.cursor() as cursor:
        cursor.execute("SELECT model_table.matchDate, model_table.cancellationofbadshot FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE (MONTH(matchDate) = MONTH(CURRENT_DATE()) AND YEAR(matchDate) = YEAR(CURRENT_DATE())) AND model_table.totalshots = '0' AND user_table.username = %s ORDER BY matchDate",[username])

        queryset = dictfetchall(cursor)
        print(queryset)
        for each in queryset:
            print(each['matchDate'])
            print(each['cancellationofbadshot'])
            labels.append(each['matchDate'])
            data.append(each['cancellationofbadshot'])
        
        return JsonResponse(data={
            'labels': labels,
            'data': data,
        })

@login_required
@permission_required('modelFormsApp.view_modelclass')
def profilesusercancellationofbadshot60shot_json(request, username):
    labels = []
    data = []
    username = username

    with connection.cursor() as cursor:
        cursor.execute("SELECT model_table.matchDate, model_table.cancellationofbadshot FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE (MONTH(matchDate) = MONTH(CURRENT_DATE()) AND YEAR(matchDate) = YEAR(CURRENT_DATE())) AND model_table.totalshots = '1' AND user_table.username = %s ORDER BY matchDate",[username])

        queryset = dictfetchall(cursor)
        print(queryset)
        for each in queryset:
            print(each['matchDate'])
            print(each['cancellationofbadshot'])
            labels.append(each['matchDate'])
            data.append(each['cancellationofbadshot'])
        
        return JsonResponse(data={
            'labels': labels,
            'data': data,
        })

@login_required
@permission_required('modelFormsApp.view_modelclass')
def profilesuserstabilityofsightpicture40shot_json(request, username):
    labels = []
    data = []
    username = username

    with connection.cursor() as cursor:
        cursor.execute("SELECT model_table.matchDate, model_table.stabilityofsightpicture FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE (MONTH(matchDate) = MONTH(CURRENT_DATE()) AND YEAR(matchDate) = YEAR(CURRENT_DATE())) AND model_table.totalshots = '0' AND user_table.username = %s ORDER BY matchDate",[username])

        queryset = dictfetchall(cursor)
        print(queryset)
        for each in queryset:
            print(each['matchDate'])
            print(each['stabilityofsightpicture'])
            labels.append(each['matchDate'])
            data.append(each['stabilityofsightpicture'])
        
        return JsonResponse(data={
            'labels': labels,
            'data': data,
        })

@login_required
@permission_required('modelFormsApp.view_modelclass')
def profilesuserstabilityofsightpicture60shot_json(request, username):
    labels = []
    data = []
    username = username

    with connection.cursor() as cursor:
        cursor.execute("SELECT model_table.matchDate, model_table.stabilityofsightpicture FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE (MONTH(matchDate) = MONTH(CURRENT_DATE()) AND YEAR(matchDate) = YEAR(CURRENT_DATE())) AND model_table.totalshots = '1' AND user_table.username = %s ORDER BY matchDate",[username])

        queryset = dictfetchall(cursor)
        print(queryset)
        for each in queryset:
            print(each['matchDate'])
            print(each['stabilityofsightpicture'])
            labels.append(each['matchDate'])
            data.append(each['stabilityofsightpicture'])
        
        return JsonResponse(data={
            'labels': labels,
            'data': data,
        })

@login_required
@permission_required('modelFormsApp.view_modelclass')
def profilesuserbodybalance40shot_json(request, username):
    labels = []
    data = []
    username = username

    with connection.cursor() as cursor:
        cursor.execute("SELECT model_table.matchDate, model_table.bodybalance FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE (MONTH(matchDate) = MONTH(CURRENT_DATE()) AND YEAR(matchDate) = YEAR(CURRENT_DATE())) AND model_table.totalshots = '0' AND user_table.username = %s ORDER BY matchDate",[username])

        queryset = dictfetchall(cursor)
        print(queryset)
        for each in queryset:
            print(each['matchDate'])
            print(each['bodybalance'])
            labels.append(each['matchDate'])
            data.append(each['bodybalance'])
        
        return JsonResponse(data={
            'labels': labels,
            'data': data,
        })

@login_required
@permission_required('modelFormsApp.view_modelclass')
def profilesuserbodybalance60shot_json(request, username):
    labels = []
    data = []
    username = username

    with connection.cursor() as cursor:
        cursor.execute("SELECT model_table.matchDate, model_table.bodybalance FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE (MONTH(matchDate) = MONTH(CURRENT_DATE()) AND YEAR(matchDate) = YEAR(CURRENT_DATE())) AND model_table.totalshots = '1' AND user_table.username = %s ORDER BY matchDate",[username])

        queryset = dictfetchall(cursor)
        print(queryset)
        for each in queryset:
            print(each['matchDate'])
            print(each['bodybalance'])
            labels.append(each['matchDate'])
            data.append(each['bodybalance'])
        
        return JsonResponse(data={
            'labels': labels,
            'data': data,
        })



@login_required
@permission_required('modelFormsApp.view_modelclass')
def profilesuserflowoftheshot40shot_json(request, username):
    labels = []
    data = []
    username = username

    with connection.cursor() as cursor:
        cursor.execute("SELECT model_table.matchDate, model_table.flowoftheshot FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE (MONTH(matchDate) = MONTH(CURRENT_DATE()) AND YEAR(matchDate) = YEAR(CURRENT_DATE())) AND model_table.totalshots = '0' AND user_table.username = %s ORDER BY matchDate",[username])

        queryset = dictfetchall(cursor)
        print(queryset)
        for each in queryset:
            print(each['matchDate'])
            print(each['flowoftheshot'])
            labels.append(each['matchDate'])
            data.append(each['flowoftheshot'])
        
        return JsonResponse(data={
            'labels': labels,
            'data': data,
        })

@login_required
@permission_required('modelFormsApp.view_modelclass')
def profilesuserflowoftheshot60shot_json(request, username):
    labels = []
    data = []
    username = username

    with connection.cursor() as cursor:
        cursor.execute("SELECT model_table.matchDate, model_table.flowoftheshot FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE (MONTH(matchDate) = MONTH(CURRENT_DATE()) AND YEAR(matchDate) = YEAR(CURRENT_DATE())) AND model_table.totalshots = '1' AND user_table.username = %s ORDER BY matchDate",[username])

        queryset = dictfetchall(cursor)
        print(queryset)
        for each in queryset:
            print(each['matchDate'])
            print(each['flowoftheshot'])
            labels.append(each['matchDate'])
            data.append(each['flowoftheshot'])
        
        return JsonResponse(data={
            'labels': labels,
            'data': data,
        })

@login_required
@permission_required('modelFormsApp.view_modelclass')
def profilesuserninetydegreetriggeroperation40shot_json(request, username):
    labels = []
    data = []
    username = username

    with connection.cursor() as cursor:
        cursor.execute("SELECT model_table.matchDate, model_table.ninetydegreetriggeroperation FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE (MONTH(matchDate) = MONTH(CURRENT_DATE()) AND YEAR(matchDate) = YEAR(CURRENT_DATE())) AND model_table.totalshots = '0' AND user_table.username = %s ORDER BY matchDate",[username])

        queryset = dictfetchall(cursor)
        print(queryset)
        for each in queryset:
            print(each['matchDate'])
            print(each['ninetydegreetriggeroperation'])
            labels.append(each['matchDate'])
            data.append(each['ninetydegreetriggeroperation'])
        
        return JsonResponse(data={
            'labels': labels,
            'data': data,
        })

@login_required
@permission_required('modelFormsApp.view_modelclass')
def profilesuserninetydegreetriggeroperation60shot_json(request, username):
    labels = []
    data = []
    username = username

    with connection.cursor() as cursor:
        cursor.execute("SELECT model_table.matchDate, model_table.ninetydegreetriggeroperation FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE (MONTH(matchDate) = MONTH(CURRENT_DATE()) AND YEAR(matchDate) = YEAR(CURRENT_DATE())) AND model_table.totalshots = '1' AND user_table.username = %s ORDER BY matchDate",[username])

        queryset = dictfetchall(cursor)
        print(queryset)
        for each in queryset:
            print(each['matchDate'])
            print(each['ninetydegreetriggeroperation'])
            labels.append(each['matchDate'])
            data.append(each['ninetydegreetriggeroperation'])
        
        return JsonResponse(data={
            'labels': labels,
            'data': data,
        })

@login_required
@permission_required('modelFormsApp.view_modelclass')
def profilesuseraverageshotduration40shot_json(request, username):
    labels = []
    data = []
    username = username

    with connection.cursor() as cursor:
        cursor.execute("SELECT model_table.matchDate, model_table.averageshotduration FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE (MONTH(matchDate) = MONTH(CURRENT_DATE()) AND YEAR(matchDate) = YEAR(CURRENT_DATE())) AND model_table.totalshots = '0' AND user_table.username = %s ORDER BY matchDate",[username])

        queryset = dictfetchall(cursor)
        print(queryset)
        for each in queryset:
            print(each['matchDate'])
            print(each['averageshotduration'])
            labels.append(each['matchDate'])
            data.append(each['averageshotduration'])
        
        return JsonResponse(data={
            'labels': labels,
            'data': data,
        })

@login_required
@permission_required('modelFormsApp.view_modelclass')
def profilesuseraverageshotduration60shot_json(request, username):
    labels = []
    data = []
    username = username

    with connection.cursor() as cursor:
        cursor.execute("SELECT model_table.matchDate, model_table.averageshotduration FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE (MONTH(matchDate) = MONTH(CURRENT_DATE()) AND YEAR(matchDate) = YEAR(CURRENT_DATE())) AND model_table.totalshots = '1' AND user_table.username = %s ORDER BY matchDate",[username])

        queryset = dictfetchall(cursor)
        print(queryset)
        for each in queryset:
            print(each['matchDate'])
            print(each['averageshotduration'])
            labels.append(each['matchDate'])
            data.append(each['averageshotduration'])
        
        return JsonResponse(data={
            'labels': labels,
            'data': data,
        })

@login_required
@permission_required('modelFormsApp.view_modelclass')
def profilesuserfollowthrough40shot_json(request, username):
    labels = []
    data = []
    username = username

    with connection.cursor() as cursor:
        cursor.execute("SELECT model_table.matchDate, model_table.followthrough FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE (MONTH(matchDate) = MONTH(CURRENT_DATE()) AND YEAR(matchDate) = YEAR(CURRENT_DATE())) AND model_table.totalshots = '0' AND user_table.username = %s ORDER BY matchDate",[username])

        queryset = dictfetchall(cursor)
        print(queryset)
        for each in queryset:
            print(each['matchDate'])
            print(each['followthrough'])
            labels.append(each['matchDate'])
            data.append(each['followthrough'])
        
        return JsonResponse(data={
            'labels': labels,
            'data': data,
        })

@login_required
@permission_required('modelFormsApp.view_modelclass')
def profilesuserfollowthrough60shot_json(request, username):
    labels = []
    data = []
    username = username

    with connection.cursor() as cursor:
        cursor.execute("SELECT model_table.matchDate, model_table.followthrough FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE (MONTH(matchDate) = MONTH(CURRENT_DATE()) AND YEAR(matchDate) = YEAR(CURRENT_DATE())) AND model_table.totalshots = '1' AND user_table.username = %s ORDER BY matchDate",[username])

        queryset = dictfetchall(cursor)
        print(queryset)
        for each in queryset:
            print(each['matchDate'])
            print(each['followthrough'])
            labels.append(each['matchDate'])
            data.append(each['followthrough'])
        
        return JsonResponse(data={
            'labels': labels,
            'data': data,
        })

@login_required
@permission_required('modelFormsApp.view_modelclass')
def profilesuservisualization40shot_json(request, username):
    labels = []
    data = []
    username = username

    with connection.cursor() as cursor:
        cursor.execute("SELECT model_table.matchDate, model_table.visualization FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE (MONTH(matchDate) = MONTH(CURRENT_DATE()) AND YEAR(matchDate) = YEAR(CURRENT_DATE())) AND model_table.totalshots = '0' AND user_table.username = %s ORDER BY matchDate",[username])

        queryset = dictfetchall(cursor)
        print(queryset)
        for each in queryset:
            print(each['matchDate'])
            print(each['visualization'])
            labels.append(each['matchDate'])
            data.append(each['visualization'])
        
        return JsonResponse(data={
            'labels': labels,
            'data': data,
        })

@login_required
@permission_required('modelFormsApp.view_modelclass')
def profilesuservisualization60shot_json(request, username):
    labels = []
    data = []
    username = username

    with connection.cursor() as cursor:
        cursor.execute("SELECT model_table.matchDate, model_table.visualization FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE (MONTH(matchDate) = MONTH(CURRENT_DATE()) AND YEAR(matchDate) = YEAR(CURRENT_DATE())) AND model_table.totalshots = '1' AND user_table.username = %s ORDER BY matchDate",[username])

        queryset = dictfetchall(cursor)
        print(queryset)
        for each in queryset:
            print(each['matchDate'])
            print(each['visualization'])
            labels.append(each['matchDate'])
            data.append(each['visualization'])
        
        return JsonResponse(data={
            'labels': labels,
            'data': data,
        })

@login_required
@permission_required('modelFormsApp.view_modelclass')
def profilesusermentalstability40shot_json(request, username):
    labels = []
    data = []
    username = username

    with connection.cursor() as cursor:
        cursor.execute("SELECT model_table.matchDate, model_table.mentalstability FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE (MONTH(matchDate) = MONTH(CURRENT_DATE()) AND YEAR(matchDate) = YEAR(CURRENT_DATE())) AND model_table.totalshots = '0' AND user_table.username = %s ORDER BY matchDate",[username])

        queryset = dictfetchall(cursor)
        print(queryset)
        for each in queryset:
            print(each['matchDate'])
            print(each['mentalstability'])
            labels.append(each['matchDate'])
            data.append(each['mentalstability'])
        
        return JsonResponse(data={
            'labels': labels,
            'data': data,
        })

@login_required
@permission_required('modelFormsApp.view_modelclass')
def profilesusermentalstability60shot_json(request, username):
    labels = []
    data = []
    username = username

    with connection.cursor() as cursor:
        cursor.execute("SELECT model_table.matchDate, model_table.mentalstability FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE (MONTH(matchDate) = MONTH(CURRENT_DATE()) AND YEAR(matchDate) = YEAR(CURRENT_DATE())) AND model_table.totalshots = '1' AND user_table.username = %s ORDER BY matchDate",[username])

        queryset = dictfetchall(cursor)
        print(queryset)
        for each in queryset:
            print(each['matchDate'])
            print(each['mentalstability'])
            labels.append(each['matchDate'])
            data.append(each['mentalstability'])
        
        return JsonResponse(data={
            'labels': labels,
            'data': data,
        })

@login_required
@permission_required('modelFormsApp.view_modelclass')
def profilesuserhydrationlevel40shot_json(request, username):
    labels = []
    data = []
    username = username

    with connection.cursor() as cursor:
        cursor.execute("SELECT model_table.matchDate, model_table.hydrationlevel FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE (MONTH(matchDate) = MONTH(CURRENT_DATE()) AND YEAR(matchDate) = YEAR(CURRENT_DATE())) AND model_table.totalshots = '0' AND user_table.username = %s ORDER BY matchDate",[username])

        queryset = dictfetchall(cursor)
        print(queryset)
        for each in queryset:
            print(each['matchDate'])
            print(each['hydrationlevel'])
            labels.append(each['matchDate'])
            data.append(each['hydrationlevel'])
        
        return JsonResponse(data={
            'labels': labels,
            'data': data,
        })

@login_required
@permission_required('modelFormsApp.view_modelclass')
def profilesuserhydrationlevel60shot_json(request, username):
    labels = []
    data = []
    username = username

    with connection.cursor() as cursor:
        cursor.execute("SELECT model_table.matchDate, model_table.hydrationlevel FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE (MONTH(matchDate) = MONTH(CURRENT_DATE()) AND YEAR(matchDate) = YEAR(CURRENT_DATE())) AND model_table.totalshots = '1' AND user_table.username = %s ORDER BY matchDate",[username])

        queryset = dictfetchall(cursor)
        print(queryset)
        for each in queryset:
            print(each['matchDate'])
            print(each['hydrationlevel'])
            labels.append(each['matchDate'])
            data.append(each['hydrationlevel'])
        
        return JsonResponse(data={
            'labels': labels,
            'data': data,
        })

@login_required
@permission_required('modelFormsApp.view_modelclass')
def profilesuserfueling40shot_json(request, username):
    labels = []
    data = []
    username = username

    with connection.cursor() as cursor:
        cursor.execute("SELECT model_table.matchDate, model_table.fueling FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE (MONTH(matchDate) = MONTH(CURRENT_DATE()) AND YEAR(matchDate) = YEAR(CURRENT_DATE())) AND model_table.totalshots = '0' AND user_table.username = %s ORDER BY matchDate",[username])

        queryset = dictfetchall(cursor)
        print(queryset)
        for each in queryset:
            print(each['matchDate'])
            print(each['fueling'])
            labels.append(each['matchDate'])
            data.append(each['fueling'])
        
        return JsonResponse(data={
            'labels': labels,
            'data': data,
        })

@login_required
@permission_required('modelFormsApp.view_modelclass')
def profilesuserfueling60shot_json(request, username):
    labels = []
    data = []
    username = username

    with connection.cursor() as cursor:
        cursor.execute("SELECT model_table.matchDate, model_table.fueling FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE (MONTH(matchDate) = MONTH(CURRENT_DATE()) AND YEAR(matchDate) = YEAR(CURRENT_DATE())) AND model_table.totalshots = '1' AND user_table.username = %s ORDER BY matchDate",[username])

        queryset = dictfetchall(cursor)
        print(queryset)
        for each in queryset:
            print(each['matchDate'])
            print(each['fueling'])
            labels.append(each['matchDate'])
            data.append(each['fueling'])
        
        return JsonResponse(data={
            'labels': labels,
            'data': data,
        })

# @login_required
# def profileuserhome(request):
#     return render(request, 'modelFormsApp/profileuserhome.html')

@login_required
def myprofile_quarterlyscore40shot_json(request):
    labels = []
    data = []

    with connection.cursor() as cursor:
        cursor.execute("SELECT model_table.matchDate, model_table.matchscore FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE DATE_ADD(CURDATE(), INTERVAL -3 MONTH) AND model_table.totalshots = '0' AND user_table.username = %s ORDER BY model_table.matchDate",[request.user])

        queryset = dictfetchall(cursor)
        print(queryset)
        for each in queryset:
            print(each['matchDate'])
            print(each['matchscore'])
            labels.append(each['matchDate'])
            data.append(each['matchscore'])
        
        return JsonResponse(data={
            'labels': labels,
            'data': data,
        })

@login_required
def myprofile_quarterlyscore60shot_json(request):
    labels = []
    data = []

    with connection.cursor() as cursor:
        cursor.execute("SELECT model_table.matchDate, model_table.matchscore FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE DATE_ADD(CURDATE(), INTERVAL -3 MONTH) AND model_table.totalshots = '1' AND user_table.username = %s ORDER BY model_table.matchDate",[request.user])

        queryset = dictfetchall(cursor)
        print(queryset)
        for each in queryset:
            print(each['matchDate'])
            print(each['matchscore'])
            labels.append(each['matchDate'])
            data.append(each['matchscore'])
        
        return JsonResponse(data={
            'labels': labels,
            'data': data,
        })

@login_required
def myprofile_quarterlybarrel40shot_json(request):
    labels = []
    data = []

    with connection.cursor() as cursor:
        cursor.execute("SELECT model_table.matchDate, model_table.flowoftheshot FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE DATE_ADD(CURDATE(), INTERVAL -3 MONTH) AND model_table.totalshots = '0' AND user_table.username = %s ORDER BY model_table.matchDate",[request.user])

        queryset = dictfetchall(cursor)
        print(queryset)
        for each in queryset:
            print(each['matchDate'])
            print(each['flowoftheshot'])
            labels.append(each['matchDate'])
            data.append(each['flowoftheshot'])
        
        return JsonResponse(data={
            'labels': labels,
            'data': data,
        })

@login_required
def myprofile_quarterlybarrel60shot_json(request):
    labels = []
    data = []

    with connection.cursor() as cursor:
        cursor.execute("SELECT model_table.matchDate, model_table.flowoftheshot FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE DATE_ADD(CURDATE(), INTERVAL -3 MONTH) AND model_table.totalshots = '1' AND user_table.username = %s ORDER BY model_table.matchDate",[request.user])

        queryset = dictfetchall(cursor)
        print(queryset)
        for each in queryset:
            print(each['matchDate'])
            print(each['flowoftheshot'])
            labels.append(each['matchDate'])
            data.append(each['flowoftheshot'])
        
        return JsonResponse(data={
            'labels': labels,
            'data': data,
        })
@login_required
def myprofile_monthlyscore40shot_json(request):
    labels = []
    data = []

    with connection.cursor() as cursor:
        cursor.execute("SELECT model_table.matchDate, model_table.matchscore FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE (MONTH(matchDate) = MONTH(CURRENT_DATE()) AND YEAR(matchDate) = YEAR(CURRENT_DATE())) AND model_table.totalshots = '0' AND user_table.username = %s ORDER BY model_table.matchDate",[request.user])

        queryset = dictfetchall(cursor)
        print(queryset)
        for each in queryset:
            print(each['matchDate'])
            print(each['matchscore'])
            labels.append(each['matchDate'])
            data.append(each['matchscore'])
        
        return JsonResponse(data={
            'labels': labels,
            'data': data,
        })

@login_required
def myprofile_monthlyscore60shot_json(request):
    labels = []
    data = []

    with connection.cursor() as cursor:
        cursor.execute("SELECT model_table.matchDate, model_table.matchscore FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE (MONTH(matchDate) = MONTH(CURRENT_DATE()) AND YEAR(matchDate) = YEAR(CURRENT_DATE())) AND model_table.totalshots = '1' AND user_table.username = %s ORDER BY model_table.matchDate",[request.user])

        queryset = dictfetchall(cursor)
        print(queryset)
        for each in queryset:
            print(each['matchDate'])
            print(each['matchscore'])
            labels.append(each['matchDate'])
            data.append(each['matchscore'])
        
        return JsonResponse(data={
            'labels': labels,
            'data': data,
        })

@login_required
@permission_required('modelFormsApp.view_modelclass')
def alluser_scorechartquarterly(request):
    labels = []
    datascore = []
    datausername = []

    with connection.cursor() as cursor:
        cursor.execute("SELECT user_table.username, model_table.matchDate, model_table.matchscore FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE DATE_ADD(CURDATE(), INTERVAL -3 MONTH) ORDER BY user_table.username, model_table.matchDate;")

        queryset = dictfetchall(cursor)
        print(queryset)
        for each in queryset:
            labels.append(each['matchDate'])
            datascore.append(each['matchscore'])
            datausername.append(each['username'])
        
        return JsonResponse(data={
            'labels': labels,
            'datascore': datascore,
            'datausername': datausername,
        })

@login_required
@permission_required('modelFormsApp.view_modelclass')
def profiles(request):
    all_users= get_user_model().objects.all()
    return render(request, 'modelFormsApp/userlist.html', {'allusers': all_users})

@login_required
def landingpage(request):
    return render(request, 'modelFormsApp/landingpage.html', {})


@login_required
@permission_required('modelFormsApp.view_modelclass')
def diary(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT user_table.username, model_table.abilityoftheday, model_table.correctionoftheday, model_table.planningforthenextpractice,model_table.matchdate FROM model_table INNER JOIN user_table ON user_table.id = model_table.shooterid_id WHERE model_table.matchDate BETWEEN DATE_SUB(CURDATE(),INTERVAL 5 WEEK) AND CURDATE() ORDER BY model_table.matchdate DESC;")
        
        diarylistdata = dictfetchall(cursor)
        p = Paginator(diarylistdata, 12)
        page_number = request.GET.get('page')
        try:
            diarylist = p.get_page(page_number)
        except PageNotAnInteger:
            diarylist = p.page(1)
        except EmptyPage:
            diarylist = p.page(p.num_pages)
        
        return render(request, 'modelFormsApp/diary.html', {'diarylist': diarylist})

@login_required
@permission_required('modelFormsApp.view_modelclass')
def technical_statistics(request):
    def pistolconsistency40shot():

        with connection.cursor() as cursor:
            cursor.execute("SELECT user_table.username as username, model_table.matchscore AS matchscore FROM model_table, user_table WHERE user_table.id = model_table.shooterid_id AND (DATE_ADD(CURDATE(), INTERVAL -3 MONTH)) AND (user_table.weapontype = '0') AND model_table.totalshots = '0' ORDER BY username;")
            technicallistdata = dictfetchall(cursor)
            
            username_list = []

            for each_dict in technicallistdata:
                pprint(each_dict)
                if each_dict['username'] not in username_list:
                    username_list.append(each_dict['username'])
            pprint(username_list)

            score_dict = {}

            for each_username in username_list:
                templistname = each_username+'_score_list'
                templistname = []
                for each_dict in technicallistdata:
                    if each_dict['username'] == each_username:
                        templistname.append(float(each_dict['matchscore']))
                score_dict[each_username] = templistname
            print(score_dict)
            dev_list = []

            for each in score_dict:
                print(score_dict[each])
                dev_dict = {}
                try:
                    dev_dict['name'] = each
                    dev_dict['deviation'] = statistics.stdev(score_dict[each])
                    slope, intercept, r_value, p_value, std_err = linregress(list(range(1, len(score_dict[each])+1)), score_dict[each])
                    dev_dict['slope'] = slope
                    dev_list.append(dev_dict)
                except:
                    pass
                del dev_dict

            pprint(dev_list)
            emerginglistdata = sorted(dev_list, key = lambda i: (i['slope']))[::-1]
            deviationlistdata = sorted(dev_list, key = lambda i: (i['deviation']))
            lackingconsistencylist = deviationlistdata[::-1]
            print(lackingconsistencylist)
            print(emerginglistdata)
            return technicallistdata, deviationlistdata, lackingconsistencylist, emerginglistdata
    def pistolconsistency60shot():

        with connection.cursor() as cursor:
            cursor.execute("SELECT user_table.username as username, model_table.matchscore AS matchscore FROM model_table, user_table WHERE user_table.id = model_table.shooterid_id AND (DATE_ADD(CURDATE(), INTERVAL -3 MONTH)) AND (user_table.weapontype = '0') AND model_table.totalshots = '1' ORDER BY username;")
            technicallistdata = dictfetchall(cursor)
            
            username_list = []

            for each_dict in technicallistdata:
                pprint(each_dict)
                if each_dict['username'] not in username_list:
                    username_list.append(each_dict['username'])
            pprint(username_list)

            score_dict = {}

            for each_username in username_list:
                templistname = each_username+'_score_list'
                templistname = []
                for each_dict in technicallistdata:
                    if each_dict['username'] == each_username:
                        templistname.append(float(each_dict['matchscore']))
                score_dict[each_username] = templistname
            print(score_dict)
            dev_list = []


            for each in score_dict:
                print(score_dict[each])
                dev_dict = {}
                try:
                    dev_dict['name'] = each
                    dev_dict['deviation'] = statistics.stdev(score_dict[each])
                    slope, intercept, r_value, p_value, std_err = linregress(list(range(1, len(score_dict[each])+1)), score_dict[each])
                    dev_dict['slope'] = slope
                    dev_list.append(dev_dict)
                except:
                    pass
                del dev_dict

            pprint(dev_list)
            emerginglistdata = sorted(dev_list, key = lambda i: (i['slope']))[::-1]
            deviationlistdata = sorted(dev_list, key = lambda i: (i['deviation']))
            lackingconsistencylist = deviationlistdata[::-1]
            print(lackingconsistencylist)
            return technicallistdata, deviationlistdata, lackingconsistencylist, emerginglistdata
    def rifleconsistency40shot():

        with connection.cursor() as cursor:
            cursor.execute("SELECT user_table.username as username, model_table.matchscore AS matchscore FROM model_table, user_table WHERE user_table.id = model_table.shooterid_id AND (DATE_ADD(CURDATE(), INTERVAL -3 MONTH)) AND (user_table.weapontype = '1') AND model_table.totalshots = '0' ORDER BY username;")
            technicallistdata = dictfetchall(cursor)
            
            username_list = []

            for each_dict in technicallistdata:
                pprint(each_dict)
                if each_dict['username'] not in username_list:
                    username_list.append(each_dict['username'])
            pprint(username_list)

            score_dict = {}

            for each_username in username_list:
                templistname = each_username+'_score_list'
                templistname = []
                for each_dict in technicallistdata:
                    if each_dict['username'] == each_username:
                        templistname.append(float(each_dict['matchscore']))
                score_dict[each_username] = templistname
            print(score_dict)
            dev_list = []

            for each in score_dict:
                print(score_dict[each])
                dev_dict = {}

                try:
                    dev_dict['name'] = each
                    dev_dict['deviation'] = statistics.stdev(score_dict[each])
                    slope, intercept, r_value, p_value, std_err = linregress(list(range(1, len(score_dict[each])+1)), score_dict[each])
                    dev_dict['slope'] = slope
                    dev_list.append(dev_dict)
                except:
                    pass
                del dev_dict


            pprint(dev_list)
            emerginglistdata = sorted(dev_list, key = lambda i: (i['slope']))[::-1]
            deviationlistdata = sorted(dev_list, key = lambda i: (i['deviation']))
            lackingconsistencylist = deviationlistdata[::-1]
            print(lackingconsistencylist)
            return technicallistdata, deviationlistdata, lackingconsistencylist, emerginglistdata
    def rifleconsistency60shot():

        with connection.cursor() as cursor:
            cursor.execute("SELECT user_table.username as username, model_table.matchscore AS matchscore FROM model_table, user_table WHERE user_table.id = model_table.shooterid_id AND (DATE_ADD(CURDATE(), INTERVAL -3 MONTH)) AND (user_table.weapontype = '1') AND model_table.totalshots = '1' ORDER BY username;")
            technicallistdata = dictfetchall(cursor)
            
            username_list = []

            for each_dict in technicallistdata:
                pprint(each_dict)
                if each_dict['username'] not in username_list:
                    username_list.append(each_dict['username'])
            pprint(username_list)

            score_dict = {}

            for each_username in username_list:
                templistname = each_username+'_score_list'
                templistname = []
                for each_dict in technicallistdata:
                    if each_dict['username'] == each_username:
                        templistname.append(float(each_dict['matchscore']))
                score_dict[each_username] = templistname
            print(score_dict)
            dev_list = []

            for each in score_dict:
                print(score_dict[each])
                dev_dict = {}
                try:
                    dev_dict['name'] = each
                    dev_dict['deviation'] = statistics.stdev(score_dict[each])
                    slope, intercept, r_value, p_value, std_err = linregress(list(range(1, len(score_dict[each])+1)), score_dict[each])
                    dev_dict['slope'] = slope
                    dev_list.append(dev_dict)
                except:
                    pass
                del dev_dict

            pprint(dev_list)
            emerginglistdata = sorted(dev_list, key = lambda i: (i['slope']))[::-1]
            deviationlistdata = sorted(dev_list, key = lambda i: (i['deviation']))
            lackingconsistencylist = deviationlistdata[::-1]
            print(lackingconsistencylist)
            return technicallistdata, deviationlistdata, lackingconsistencylist, emerginglistdata
    pistol40shotlist = pistolconsistency40shot()
    pistoltechnicallist40shotdata = pistol40shotlist[0]
    pistoldeviationlist40shotdata = pistol40shotlist[1]
    pistollackingconsistency40shotlist = pistol40shotlist[2]
    pistolemerging40shotlist = pistol40shotlist[3]
    rifle40shotlist = rifleconsistency40shot()
    rifletechnicallist40shotdata = rifle40shotlist[0]
    rifledeviationlist40shotdata = rifle40shotlist[1]
    riflelackingconsistency40shotlist = rifle40shotlist[2]
    rifleemerging40shotlist = rifle40shotlist[3]
    pistol60shotlist = pistolconsistency60shot()
    pistoltechnicallist60shotdata = pistol60shotlist[0]
    pistoldeviationlist60shotdata = pistol60shotlist[1]
    pistollackingconsistency60shotlist = pistol60shotlist[2]
    pistolemerging60shotlist = pistol60shotlist[3]
    rifle60shotlist = rifleconsistency60shot()
    rifletechnicallist60shotdata = rifle60shotlist[0]
    rifledeviationlist60shotdata = rifle60shotlist[1]
    riflelackingconsistency60shotlist = rifle60shotlist[2]
    rifleemerging60shotlist = rifle60shotlist[3]
    return render(request, 'modelFormsApp/technical_statistics.html', {'pistoltechnicallist40shotdata': pistoltechnicallist40shotdata, 'pistoldeviationlist40shotdata': pistoldeviationlist40shotdata, 'pistollackingconsistency40shotlist': pistollackingconsistency40shotlist, 'pistolemerging40shotlist': pistolemerging40shotlist, 'rifletechnicallist40shotdata': rifletechnicallist40shotdata, 'rifledeviationlist40shotdata': rifledeviationlist40shotdata, 'riflelackingconsistency40shotlist': riflelackingconsistency40shotlist, 'rifleemerging40shotlist': rifleemerging40shotlist, 'pistoltechnicallist60shotdata': pistoltechnicallist60shotdata, 'pistoldeviationlist60shotdata': pistoldeviationlist60shotdata, 'pistollackingconsistency60shotlist': pistollackingconsistency60shotlist, 'pistolemerging60shotlist': pistolemerging60shotlist, 'rifletechnicallist60shotdata': rifletechnicallist60shotdata, 'rifledeviationlist60shotdata': rifledeviationlist60shotdata, 'riflelackingconsistency60shotlist': riflelackingconsistency60shotlist, 'rifleemerging60shotlist': rifleemerging60shotlist})