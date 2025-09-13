from django.db import models
from admin_app.models import Car, Layout, Campaign
from django.utils import timezone

class Driver(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, unique=True, db_index=True)
    date_maj = models.DateTimeField(default=timezone.now, db_index=True)

    def __str__(self):
        return self.name

class LapTime(models.Model):
    id = models.CharField(primary_key=True, max_length=64, editable=False)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='lap_times')
    layout = models.ForeignKey(Layout, on_delete=models.CASCADE, related_name='lap_times')
    car = models.ForeignKey(Car, on_delete=models.CASCADE,related_name='lap_times')
    lap_time_ms = models.PositiveIntegerField(help_text="Temps au tour en millisecondes")
    date_maj = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        # Unicité du triplet driver/layout/car
        constraints = [
            models.UniqueConstraint(
                fields=['driver', 'layout', 'car'],
                name='uniq_driver_layout_car'
            )
        ]
        # Index utiles pour les requêtes fréquentes
        indexes = [
            models.Index(fields=['layout', 'car', 'lap_time_ms']),
            models.Index(fields=['layout', 'driver', 'car', 'lap_time_ms'])
        ]
        ordering = ['layout', 'car', 'lap_time_ms']

    def __str__(self):
        return f"{self.driver_name} • {self.layout} • {self.car} → {self.formatted_time}"

    def _make_id(self) -> str:
        # format stable et compact (évite les collisions)
        return f"d{self.driver_id}-l{self.layout_id}-c{self.car_id}"

    def save(self, *args, **kwargs):
        # Assure que la PK est toujours cohérente avec les FK
        if self.driver_id and self.layout_id and self.car_id:
            self.id = self._make_id()
        super().save(*args, **kwargs)

    @property
    def formatted_time(self) -> str:
        """Retourne le temps au format M:SS.mmm (ex: 1:42.357)."""
        total_ms = int(self.lap_time_ms or 0)
        minutes, rem_s = divmod(total_ms // 1000, 60)
        ms = total_ms % 1000
        return f"{minutes}:{rem_s:02d}.{ms:03d}"

class Medal(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    coef =  models.FloatField(default=2)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.name
