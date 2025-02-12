from django.db import models
from django.contrib.auth.models import User


class Item(models.Model):
    serial_number = models.CharField(max_length=100, unique=False, verbose_name="Серийный номер")
    description = models.TextField(verbose_name="Описание")
    owner = models.CharField(max_length=100, verbose_name="Кому принадлежит")
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата окончания")

    def __str__(self):
        return f"{self.serial_number} - {self.owner}"
# Create your models here.
