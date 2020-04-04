from django.db import models


# Create your models here.
class Fruits(models.Model):
    """评论"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, verbose_name=u"名称")
    checkstate = models.BooleanField(verbose_name=u"状态")

    class Meta:
        verbose_name = u"水果"
        verbose_name_plural = verbose_name
