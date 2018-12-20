from django.db import models


class Alpha(models.Model):

    dummy = models.CharField(max_length=10, default='')
    new_field = models.CharField(max_length=10, default='')


class Bravo(models.Model):

    dummy = models.CharField(max_length=10, default='')
    alpha = models.ForeignKey('app.Alpha', on_delete=models.CASCADE)
