from django.db import models


class Wallet(models.Model):
    """Модель кошелька"""
    currency = models.CharField(max_length=3, verbose_name='Валюта')
    private_key = models.CharField(max_length=66, verbose_name='Приватный ключ', unique=True)
    public_key = models.CharField(max_length=44, verbose_name='Публичный ключ', unique=True)

    def __str__(self):
        return self.public_key
