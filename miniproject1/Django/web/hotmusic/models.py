from django.db import models

class TOP(models.Model):
    object = models.Manager()   #vscode 오류 제거용
    site = models.CharField(max_length=20) #VARCHAR2 20
    day = models.CharField(max_length=20) #VARCHAR2 20
    hour = models.CharField(max_length=20) #VARCHAR2 20
    rank = models.CharField(max_length=10) #VARCHAR2 10
    title = models.CharField(max_length=200) #VARCHAR2 200
    artist = models.CharField(max_length=200) #VARCHAR2 200
    image = models.CharField(max_length=300, default="album") #VARCHAR2 300

class TWEET(models.Model) :
    object = models.Manager()
    t_title = models.CharField(max_length=200)
    t_artist = models.CharField(max_length=200)
    t_day = models.CharField(max_length=20)
    t_count = models.IntegerField()