from django.test import TestCase
from wallet_manager.models import Wallet


class WalletModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Wallet.objects.get_or_create(
            currency='ETH',
            private_key='0xabcdef1234567890',
            public_key='0x1234567890abcdef',
        )

    def test_currency_max_length(self):
        # Проверяем, что максимальная длина поля currency задана корректно
        wallet = Wallet.objects.all().first()
        max_length = wallet._meta.get_field('currency').max_length
        self.assertEqual(max_length, 3)

    def test_private_key_max_length(self):
        # Проверяем, что максимальная длина поля private_key задана корректно
        wallet = Wallet.objects.all().first()
        max_length = wallet._meta.get_field('private_key').max_length
        self.assertEqual(max_length, 66)

    def test_public_key_max_length(self):
        # Проверяем, что максимальная длина поля public_key задана корректно
        wallet = Wallet.objects.all().first()
        max_length = wallet._meta.get_field('public_key').max_length
        self.assertEqual(max_length, 44)

    def test_private_key_unique(self):
        # Проверяем, что поле private_key является уникальным
        wallet = Wallet(
            currency='ETH',
            private_key='0xabcdef1234567890',
            public_key='0x1234567890abcdef',
        )
        with self.assertRaises(Exception):
            wallet.save()

    def test_public_key_unique(self):
        # Проверяем, что поле public_key является уникальным
        wallet = Wallet(
            currency='ETH',
            private_key='0xabcdef1234567890',
            public_key='0x1234567890abcdef',
        )
        with self.assertRaises(Exception):
            wallet.save()

    def test_str_method(self):
        # Проверяем, что метод __str__ возвращает публичный ключ
        wallet = Wallet.objects.all().first()
        self.assertEqual(str(wallet), '0x1234567890abcdef')
