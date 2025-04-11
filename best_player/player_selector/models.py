from django.db import models
from accounts.models import User

class Place(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name
class Time(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name
class Field(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name        

class BestHomo(models.Model):
    name = models.CharField(max_length=255)
    time = models.ManyToManyField(Time)
    field = models.ManyToManyField(Field)
    place = models.ManyToManyField(Place)

    def __str__(self):
        return self.name

class Vote(models.Model):
    player = models.ForeignKey(BestHomo, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user} voted for {self.player}"