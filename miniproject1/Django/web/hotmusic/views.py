from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from .models import TOP, TWEET
import operator

def home(request):
    if request.method == 'GET':
        return render(request, 'hotmusic/home.html')

@csrf_exempt
def musicchart(request):
    if request.method == 'GET':
        site = request.GET.get("site", 'melon')
        day = '1218'
        hour= '10'
        mo = day[:2]
        da = day[2:]
        obj = TOP.object.all().filter(site=site, day=day, hour=hour).order_by('id')
        obj1=list(obj)
        return render(request, 'hotmusic/musicchart.html', {'data':obj1, 'mo':mo, 'da':da})

    elif request.method == "POST":
        site=request.POST['site']
        day=request.POST['day']
        mo = day[:2]
        da = day[2:]
        hour = request.POST['hour']
        title_name = request.POST['title_name']

        if title_name != None:
            print(site, day, hour, title_name)
            obj_post = TOP.object.all().filter(site=site,  day=day, hour=hour, title__icontains=title_name).order_by('id')
            obj2=list(obj_post)
         
        elif title_name == None:
            print(site, day, hour, title_name)
            obj_post = TOP.object.all().filter(site=site, day=day, hour=hour).order_by('id')
            obj2=list(obj_post)
        
        return render(request, 'hotmusic/musicchart.html', {'data':obj2, 'mo':mo, 'da':da})

def ranking(request):  
    if request.method == 'GET':
        site = request.GET.get("site", 'melon')
        day = request.GET.get("day", '')
        mo = day[:2]
        da = day[2:]
        hour = request.GET.get("hour", '')
        title = request.GET.get("title", '')
        rank = request.GET.get("rank", '')
        obj = TOP.object.filter(site=site, day=day, hour=hour, title__icontains=title, rank=rank)
        
        obj_genie = TOP.object.filter(site='genie', day=day, hour=hour, title=title)
        obj_melon = TOP.object.filter(site='melon', day=day, hour=hour, title__icontains=title)
        obj_bugs = TOP.object.filter(site='bugs', day=day, hour=hour, title=title)

        return render(request, 'hotmusic/ranking.html', {'data':obj, 'data_genie':obj_genie, 'data_melon':obj_melon, 'data_bugs':obj_bugs, 'mo':mo, 'da':da})

@csrf_exempt
def zzinchart(request):  
    if request.method == 'GET':
        zzinchart = {}
        day = request.GET.get("day", '1218')
        mo = day[:2]
        da = day[2:]
        bugs = TOP.object.filter(day=day, hour='10', site='bugs')
        for top in bugs:
            zzinchart[top.title] = 101 - int(top.rank)
        
        bugs_titles = list(zzinchart.keys())
        for b_title in bugs_titles:
            melon = TOP.object.filter(day=day, hour='10', site='melon', title__icontains=b_title)
            try:
                zzinchart[b_title] += (101 - int(melon[0].rank))
            except:
                pass
            genie = TOP.object.filter(day=day, hour='10', site='genie', title__icontains=b_title)
            try:
                zzinchart[b_title] += (101 - int(genie[0].rank))
            except:
                pass
            tweets = TWEET.object.filter(t_day=day, t_title=b_title)
            try:
                count = int(tweets[0].t_count)
                if count == 0:
                    zzinchart[b_title] *= 0.8
                elif 1<= count <=5 :
                    zzinchart[b_title] *= 0.85
                elif 6<= count <=10 :
                    zzinchart[b_title] *= 0.9
                elif 11<= count <=30 :
                    zzinchart[b_title] *= 0.95
                elif 31<= count <=50 :
                    pass
                elif 51<= count <=70 :
                    zzinchart[b_title] *= 1.05
                elif 71<= count <=90 :
                    zzinchart[b_title] *= 1.1
                elif 90<= count :
                    zzinchart[b_title] *= 1.15
            except:
                pass
        data= sorted(zzinchart.items(), key=operator.itemgetter(1), reverse=True)
       
        rank = []
        for i, j in enumerate(data):
            rank.append([i+1,j])

        return render(request, 'hotmusic/zzinchart.html', {'data':rank, 'day':day, 'mo':mo, 'da':da} )

    elif request.method == "POST":
        zzin_day=request.POST['zzin_day']
        mo = zzin_day[:2]
        da = zzin_day[2:]
        zzinchart = {}
        bugs = TOP.object.filter(day=zzin_day, hour='10', site='bugs')
        for top in bugs:
            zzinchart[top.title] = 101 - int(top.rank)
        
        bugs_titles = list(zzinchart.keys())
        for b_title in bugs_titles:
            melon = TOP.object.filter(day=zzin_day, hour='10', site='melon', title__icontains=b_title)
            try:
                zzinchart[b_title] += (101 - int(melon[0].rank))
            except:
                pass
            genie = TOP.object.filter(day=zzin_day, hour='10', site='genie', title__icontains=b_title)
            try:
                zzinchart[b_title] += (101 - int(genie[0].rank))
            except:
                pass
            tweets = TWEET.object.filter(t_day=zzin_day, t_title=b_title)
            try:
                count = int(tweets[0].t_count)
                if count == 0:
                    zzinchart[b_title] *= 0.8
                elif 1<= count <=5 :
                    zzinchart[b_title] *= 0.85
                elif 6<= count <=10 :
                    zzinchart[b_title] *= 0.9
                elif 11<= count <=30 :
                    zzinchart[b_title] *= 0.95
                elif 31<= count <=50 :
                    pass
                elif 51<= count <=70 :
                    zzinchart[b_title] *= 1.05
                elif 71<= count <=90 :
                    zzinchart[b_title] *= 1.1
                elif 90<= count :
                    zzinchart[b_title] *= 1.15
            except:
                pass

        data= sorted(zzinchart.items(), key=operator.itemgetter(1), reverse=True)

        rank = []
        for i, j in enumerate(data):
            rank.append([i+1,j])

        return render(request, 'hotmusic/zzinchart.html', {'data':rank,'day':zzin_day,'mo':mo, 'da':da} )

def zzinranking(request):  
    if request.method == 'GET':
        day = request.GET.get("day", '')
        tmp1 = day[:2]
        tmp2 = day[2:]
        title = request.GET.get("title", '')
        zzinchart = {}
        bugs = TOP.object.filter(day=day, hour='10', site='bugs')
        for top in bugs:
            zzinchart[top.title] = 101 - int(top.rank)
        
        bugs_titles = list(zzinchart.keys())
        for b_title in bugs_titles:
            melon = TOP.object.filter(day=day, hour='10', site='melon', title__icontains=b_title)
            try:
                zzinchart[b_title] += (101 - int(melon[0].rank))
            except:
                pass
            genie = TOP.object.filter(day=day, hour='10', site='genie', title__icontains=b_title)
            try:
                zzinchart[b_title] += (101 - int(genie[0].rank))
            except:
                pass
            tweets = TWEET.object.filter(t_day=day, t_title=b_title)
            try:
                count = int(tweets[0].t_count)
                if count == 0:
                    zzinchart[b_title] *= 0.8
                elif 1<= count <=5 :
                    zzinchart[b_title] *= 0.85
                elif 6<= count <=10 :
                    zzinchart[b_title] *= 0.9
                elif 11<= count <=30 :
                    zzinchart[b_title] *= 0.95
                elif 31<= count <=50 :
                    pass
                elif 51<= count <=70 :
                    zzinchart[b_title] *= 1.05
                elif 71<= count <=90 :
                    zzinchart[b_title] *= 1.1
                elif 90<= count :
                    zzinchart[b_title] *= 1.15
            except:
                pass
        data= sorted(zzinchart.items(), key=operator.itemgetter(1), reverse=True)

        zzin_rank = 0
        for i, j in enumerate(data):
            if j[0]==title:
                zzin_rank= int(i)+1
        
        return render(request, 'hotmusic/zzinranking.html',{'day':day,'title':title, 'rank':zzin_rank, 'tmp1':tmp1, 'tmp2':tmp2})