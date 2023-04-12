from decimal import Decimal

from django.test import TestCase

from wallet_manager.models import Wallet
from wallet_manager.serializers import WalletSerializer, WalletTransactionSerializer


class WalletSerializerTestCase(TestCase):
    def setUp(self):
        self.wallet_data = {
            'currency': 'ETH',
            'private_key': 'test_private_key',
            'public_key': 'test_public_key'
        }
        self.wallet = Wallet.objects.create(**self.wallet_data)

    def test_wallet_serializer(self):
        serializer = WalletSerializer(self.wallet)
        expected_data = {
            'id': self.wallet.id,
            'currency': self.wallet.currency,
            'public_key': self.wallet.public_key,
        }
        self.assertEqual(serializer.data, expected_data)


class WalletTransactionSerializerTestCase(TestCase):
    def setUp(self):

        wallet1 = Wallet.objects.create(
            currency='ETH',
            public_key='test_public_key1',
            private_key='test_private_key1',
        )

        wallet2 = Wallet.objects.create(
            currency='ETH',
            public_key='test_public_key2',
            private_key='test_private_key2',
        )

        self.data = {
            'from': wallet1.public_key,
            'to': wallet2.public_key,
            'amount': '0.1',
            'currency': 'ETH',
        }

    def test_wallet_transaction_serializer(self):
        serializer = WalletTransactionSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['from'], self.data['from'])
        self.assertEqual(serializer.validated_data['to'], self.data['to'])
        self.assertEqual(serializer.validated_data['amount'], Decimal(self.data['amount']))
        self.assertEqual(serializer.validated_data['currency'], self.data['currency'])

    def test_wallet_transaction_serializer_validate_same_address(self):
        self.data['from'] = self.data['to']
        serializer = WalletTransactionSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors['from'], ['Нельзя отправлять транзакцию самому себе'])
