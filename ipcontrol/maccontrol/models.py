from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class MacAddress(models.Model):
    name = models.CharField(max_length=256)
    mac_address = models.CharField(max_length=17)
    authorized = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    allowed_days = models.DateTimeField(null=False,blank=False)
    created_at = models.DateTimeField(default=timezone.now)


    def __str__(self) -> str:
        return self.name