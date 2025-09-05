from django.db import models

class Class(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Car(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    carClass = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="cars")

    def __str__(self):
        return self.name


class Track(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Layout(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name="layouts")

    def __str__(self):
        return f"{self.track.name} - {self.name}"


class Campaign(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    cars = models.ManyToManyField(Car, related_name="campaigns", blank=True)
    layouts = models.ManyToManyField(Layout, related_name="campaigns", blank=True)

    def __str__(self):
        return self.name
