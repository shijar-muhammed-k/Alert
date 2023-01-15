from django.db import models

# Create your models here.
class ship_details(models.Model):
    name = models.CharField(max_length=25)
    address = models.CharField(max_length=100)
    email = models.EmailField(max_length=25)
    phone = models.CharField(max_length=15)
    docking_date = models.DateField()
    undocking_date = models.DateField()
    reminder_type = models.CharField(max_length=10)
    reminder_date = models.DateField()
    reminder_days = models.IntegerField()
    status = models.CharField(max_length=25, null=True, blank=True)

    def meta():
        db_table = 'ship_details'