from django.db import models

class Class(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Car(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    class_ref = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="cars")

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
    track_ref = models.ForeignKey(Track, on_delete=models.CASCADE, related_name="layouts")

    def __str__(self):
        return f"{self.track_ref.name} - {self.name}"