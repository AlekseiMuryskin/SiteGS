import datetime

from django.db import models

# Create your models here.


class DataRequester(models.Model):
    email = models.EmailField(max_length=200)


class DataRequesterPersonal (models.Model):
    data_requester = models.ForeignKey(DataRequester, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)


class DataRequesterPhone (models.Model):
    data_requester_personal = models.ForeignKey(DataRequesterPersonal, on_delete=models.CASCADE)
    phone = models.CharField(max_length = 30)


class RequesterOrganization (models.Model):
    data_requester_personal = models.ForeignKey(DataRequesterPersonal, on_delete=models.CASCADE)
    name = models.CharField(max_length=1024, default='organization')


class RequesterOrganizationBoss(models.Model):
    requester_organization = models.ForeignKey(RequesterOrganization, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)


class RequestData(models.Model):
    data_requester = models.ForeignKey(DataRequester,  on_delete=models.CASCADE)
    date_time_create = models.DateTimeField(auto_now_add=True)
    request_file = models.FilePathField()
    commentary_to_file = models.TextField(null=True)
    type_data = models.CharField(max_length=200)
    basis = models.TextField(null=True)


class Organization (models.Model):
    parent = models.IntegerField()
    position = models.CharField(max_length=512)
    href = models.URLField (default="#")


class News (models.Model):
    title = models.CharField(null=False, max_length=512)
    body = models.TextField (null= True)
    created = models.DateField (default = datetime.datetime.now)

    class Meta:
        verbose_name_plural = "Новостная лента"


class NewsImageContent (models.Model):
    news = models.OneToOneField(News, on_delete=models.CASCADE)
    image_storage = models.ImageField(null=True)

    class Meta:
        verbose_name = "Добавить изображение"

class NewsMapPointFloat (models.Model):
    news = models.OneToOneField(News, on_delete=models.CASCADE)
    lon = models.FloatField(null=True)
    lat = models.FloatField(null=True)

    class Meta:
        verbose_name = "Добавить координаты события"




