from django.contrib.auth.models import User
from django.db import models

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.urls import reverse


class Companies(models.Model):
    title = models.CharField(max_length=7)
    companies = models.CharField(max_length=15)
    comments = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    money = models.DecimalField(decimal_places=10, max_digits=11, max_length=2, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Companies'
        # Бинарное дерево поиска
        indexes = [
            models.Index(
                name='Companies_date_time_idx',
                fields=['date']
            )
        ]

    def get_absolute_url(self):
        return reverse('get_post', kwargs={'post_id': self.pk})

    def __str__(self):
        return 'Companies:' + self.title


class Log(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    obj = models.CharField('model', max_length=10)
    message = models.CharField(max_length=300)

    class Meta:
        db_table = 'posts_logs'
        indexes = [
            models.Index(fields=['datetime'], name='datetime_index')
        ]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    car = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'auth_user_profile'
