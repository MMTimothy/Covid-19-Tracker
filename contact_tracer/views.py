import datetime
import json

from django.core import serializers
from django.shortcuts import render,redirect
from django.views import generic
from django.shortcuts import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from .models import *
import base64

# Create your views here.


class Index(generic.FormView):
    def get(self, request, *args, **kwargs):
        if request.user.id is None:
            return render(request,'index.html')
        else:
            return redirect('login')

class Login(generic.FormView):
    def get(self, request, *args, **kwargs):
        return render(request,'login.html')
    def post(self, request, *args, **kwargs):
        form = request.POST
        username = form["username"]
        password = form["password"]

        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
        else:
            pass
        return HttpResponse(0)

class COVIDStatistics(generic.FormView):
    def get(self, request, *args, **kwargs):
        covidCases = CovidCases.objects.all()
        context = {
            "cases":covidCases
        }
        return render(request,'covid_statistics.html',context)
    def post(self, request, *args, **kwargs):
        form = request.POST
        province = form["province"]
        cases = form["cases"]
        recoveries = form["recoveries"]
        fatalities = form["fatalities"]
        date = form["date"]

        CovidCases.objects.create(province=province,cases=cases,recoveries=recoveries,fatalities=fatalities,date=date)

        return HttpResponse(0)

@method_decorator(csrf_exempt,name='dispatch')
class PostProvinces(generic.FormView):
    def post(self, request, *args, **kwargs):
        form = request.POST
        province = form["Province"]

        Provinces.objects.create(province=province)
        return HttpResponse(0)

@method_decorator(csrf_exempt,name="dispatch")
class GetProvinces(generic.FormView):
    def post(self, request, *args, **kwargs):
        form = request.POST
        serversId = json.loads(form["ServerId"])
        ids = []
        for serverId in serversId:
            print(serverId)
            ids.append(serverId["ServerId"])
        provinces = Provinces.objects.all().exclude(id__in=ids)
        provinces = serializers.serialize("json",provinces)
        return HttpResponse(provinces)

@method_decorator(csrf_exempt,name='dispatch')
class GetCases(generic.FormView):
    def get(self, request, *args, **kwargs):
        covidCases = CovidCases.objects.all()
        cases = serializers.serialize("json",covidCases)

        return HttpResponse(cases)
    def post(self, request, *args, **kwargs):
        form = request.POST
        serversId = form["ServerId"]
        serversId = json.loads(serversId)
        ids = []
        for serverId in serversId:
            ds = serverId["ServerId"]
            ids.append(ds)

        print(ids)
        covidCases = CovidCases.objects.all().exclude(id__in=ids)
        cases = serializers.serialize("json", covidCases)

        return HttpResponse(cases)

@method_decorator(csrf_exempt,name='dispatch')
class SendContact(generic.FormView):
    def post(self, request, *args, **kwargs):
        form = request.POST
        results = form["Results"]
        date = form["DateResults"]
        contacts = form["Contacts"]
        contacts_data = json.loads(contacts)
        for cont in contacts_data:
            hostAddress = cont["HostAddress"]
            contactAddress = cont["ContactAddress"]
            dateContacts = cont["Date"]
            hostInfo = hostAddress.split(":")
            hostAddressOUI = hostInfo[:3]
            hostAddressVA = hostInfo[3:]
            contactInfo = contactAddress.split(":")
            contactAddressOUI = contactInfo[:3]
            contactAddressVA = contactInfo[3:]
            contactDate = datetime.datetime.fromtimestamp(int(dateContacts)/1000).strftime("%d-%m-%Y %H:%M:%S")

            contact = Contacts.objects.create(hostAddressOUI=hostAddressOUI,hostAddressVA=hostAddressVA,contactAddressOUI=contactAddressOUI,contactAddressVA=contactAddressVA)
        print(results)
        return HttpResponse(0)

@method_decorator(csrf_exempt,name='dispatch')
class CheckContact(generic.FormView):
    def post(self, request, *args, **kwargs):
        form = request.POST
        hostAddress = form["HostAddress"]
        hostAddress = hostAddress.split(":")
        hostAddressOUI = hostAddress[:3]
        contact = Contacts.objects.all().filter(contactAddressOUI=hostAddressOUI)
        #print(hostAddressOUI)
        #print(len(contact))
        #print(hostAddress)
        hostLen = len(contact)
        return HttpResponse(hostLen)

class PostNews(generic.FormView):
    def post(self, request, *args, **kwargs):
        form = request.POST
        title=form["title"]
        body = form["body"]
        newsThumbnail = request.FILES["newsThumbnail"]
        NewsThumbnail = base64.b64encode(newsThumbnail.read())
        print(type(NewsThumbnail))

        covidNews = CovidNews.objects.create(title=title,body=body,thumbnail=NewsThumbnail.decode("utf-8"))
        print("Successfully Saved")
        return HttpResponse(0)

@method_decorator(csrf_exempt,name="dispatch")
class GetNews(generic.FormView):
    def post(self, request, *args, **kwargs):
        form = request.POST
        newsId = form["NewsId"]
        newsData = json.loads(newsId)
        print(newsId)
        newsList = list()
        for news in newsData:
            id = news["ServerId"]
            newsList.append(id)
        covidNews = CovidNews.objects.all().exclude(id__in = newsList)[:2]
        covidNews = serializers.serialize("json",covidNews)
        return HttpResponse(covidNews)
