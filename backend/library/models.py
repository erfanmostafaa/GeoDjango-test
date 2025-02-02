from django.db import models
from user.models import User
from django.contrib.gis.db import models as gis_models


class Book(models.Model):
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=150)
    price =models.DecimalField(max_digits=10 , decimal_places=2)
    available = models.BooleanField(default=True)


    def __str__(self):
        return self.title
    

class Purchase(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='purchases')
    book = models.ForeignKey(Book , on_delete=models.CASCADE , related_name='purchases')
    purchase_at = models.DateTimeField(default=True)

    def __str__(self):
        return f'{self.user} - {self.book.title}'
    






class Province(models.Model):
    objectid = models.IntegerField(null=True , blank=True)
    area = models.FloatField(null=True , blank=True)
    perimeter = models.FloatField(null=True , blank=True)
    pzanj_field = models.FloatField(null=True , blank=True)
    pzanj_id = models.FloatField(null=True , blank=True)
    sourcethm = models.CharField(max_length=16 ,null=True , blank=True)
    acres = models.FloatField(null=True , blank=True)
    shape_leng = models.FloatField(null=True , blank=True)
    shape_area = models.FloatField(null=True , blank=True)
    ostn_name = models.CharField(max_length=20 ,null=True , blank=True)
    code = models.IntegerField(null=True , blank=True)
    areaasss = models.CharField(max_length=50 ,null=True , blank=True)
    areaaqqqqq = models.FloatField(null=True , blank=True)
    per = models.FloatField(null=True , blank=True)
    codeddd = models.IntegerField(null=True , blank=True)
    ara = models.FloatField(null=True , blank=True)
    geom = gis_models.MultiPolygonField(srid=4326 ,null=True , blank=True)

