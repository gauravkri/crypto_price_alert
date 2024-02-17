from django.db import models

# Create your models here.



STATUS_CHOICE = [('created', 'created'), ('disabled', "disabled")]


class Alert(models.Model):
    coin_id = models.CharField(max_length=100, blank=False)
    alert_name = models.CharField(max_length=100, blank=False)
    alert_price = models.CharField(max_length=100, blank=False)
    status = models.CharField(
        choices=STATUS_CHOICE, default="created", max_length=100
    )

    createdAt = models.DateTimeField(auto_now_add=True)
    createdBy = models.IntegerField(max_length=100)

    def __str__(self):
        return self.alert_name