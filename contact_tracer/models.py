from django.db import models

# Create your models here.


class Contacts(models.Model):
    hostAddressOUI = models.CharField(max_length=250, null=True)
    hostAddressVA = models.CharField(max_length=250, null=True)
    contactAddressOUI = models.CharField(max_length=250, null=True)
    contactAddressVA = models.CharField(max_length=250, null=True)
    date = models.CharField(max_length=250, null=True)

class CovidFacts(models.Model):
    title = models.CharField(max_length=250,null=True)
    body = models.TextField(null=True)
class CovidNews(models.Model):
    title = models.CharField(max_length=250,null=True)
    body = models.TextField(null=True)
    thumbnail = models.TextField(null=True)

class CovidCases(models.Model):
    province = models.CharField(max_length=250,null=True)
    cases = models.CharField(max_length=250,null=True)
    recoveries = models.CharField(max_length=250,null=True)
    fatalities = models.CharField(max_length=250,null=True)
    date = models.CharField(max_length=250,null=True)

class Provinces(models.Model):
    province = models.CharField(max_length=250,null=True)


