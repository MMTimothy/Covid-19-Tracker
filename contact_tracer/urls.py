from django.urls import path
from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("login",views.Login.as_view(),name="login"),
    path("get_cases",views.GetCases.as_view(),name="getCases"),
    path("post_province",views.PostProvinces.as_view(),name="postProvince"),
    path("get_province",views.GetProvinces.as_view(),name="getProvince"),
    path("covid_statistics",views.COVIDStatistics.as_view(),name="covidStatistics"),
    path("send_contacts", views.SendContact.as_view(), name="sendContact"),
    path("check_contact",views.CheckContact.as_view(),name="checkContact"),
    path("post_news",views.PostNews.as_view(),name="postNews"),
    path("get_news",views.GetNews.as_view(),name="getNews")

]
