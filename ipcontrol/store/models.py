from django.db import models


class Store(models.Model):
    name = models.CharField(max_length=30,blank=False,null=False)
    concentrator = models.CharField(max_length=16,blank=False,null=False)
    gateway = models.CharField(max_length=16,blank=False,null=False)
    details = models.TextField()


class Pdv(models.Model):
    store = models.ForeignKey(Store, models.CASCADE, related_name='pdvs',blank=False,null=False)
    nfce = models.CharField(max_length=2,blank=False,null=False)
    ip = models.CharField(max_length=16,blank=False,null=False)

    def __str__(self):
        return self.nfce