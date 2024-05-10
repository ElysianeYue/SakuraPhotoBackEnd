from django.db import models

class Image(models.Model):
    id = models.AutoField(primary_key=True)
    img_name = models.CharField(max_length=100)
    img_size = models.CharField(max_length=20)
    img_down_link = models.URLField(max_length=200)
    weight = models.IntegerField(default=1)
    sort = models.IntegerField(default=0)
    uploader = models.IntegerField(default=10000)

    def __str__(self):
        return self.img_name

    class Meta:
        app_label = 'paper'
class Sort(models.Model):
    id = models.AutoField(primary_key=True)
    sortName = models.CharField(max_length=10)
    firstPaper = models.CharField(max_length=100)

    def __str__(self):
        return self.sortName

    class Meta:
        app_label = 'paper'