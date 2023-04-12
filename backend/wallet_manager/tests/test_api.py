import json
from unittest.mock import patch

from django.shortcuts import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from wallet_manager.managers import CryptoManager
from wallet_manager.models import Wallet


class WalletViewTestCase(APITestCase):

    def setUp(self):
        self.wallets_url = reverse('wallets_v1')
        self.transaction_url = reverse('transaction_v1')

        # Список валют, которые поддерживаются менеджером,
        # в дальнейшем можно вынести в модель или в настройки
        self.currency_names = ['ETH', ]
        self.fake_currency_name = 'FKE'
        self.fake_currency_name_long = 'FAKE'

    @patch.object(CryptoManager, 'get_new_account')
    def test_create_wallet_success(self, mock_get_new_account):
        """
        Тест на успешное создание кошелька
        """

        # Замокаем метод get_new_account
        mock_get_new_account.return_value = {'public_key': 'test_public_key', 'private_key': 'test_private_key'}

        data = {'currency': self.currency_names[0]}

        response = self.client.post(self.wallets_url, data, format='json')

        # Проверяем, что был вызван метод get_new_account
        mock_get_new_account.assert_called_once_with()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        wallet = Wallet.objects.get(public_key='test_public_key')
        self.assertEqual(wallet.currency, 'ETH')
        self.assertEqual(wallet.public_key, 'test_public_key')
        self.assertEqual(wallet.private_key, 'test_private_key')

    @patch.object(CryptoManager, 'get_new_account')
    def test_create_wallet_invalid_currency_standard(self, mock_get_new_account):
        """
        Тест на создание кошелька с неверной валютой стандартной длины
        """

        # Замокаем метод get_new_account
        mock_get_new_account.side_effect = ValueError(f'Валюта {self.fake_currency_name} не поддерживается')

        data = {'currency': self.fake_currency_name}

        response = self.client.post(self.wallets_url, data, format='json')

        # Проверяем, что был вызван метод get_new_account не был вызван
        mock_get_new_account.assert_not_called()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        content = json.loads(response.content.decode())
        self.assertEqual(content['error'], f'Валюта {self.fake_currency_name} не поддерживается')

    @patch.object(CryptoManager, 'get_new_account')
    def test_create_wallet_invalid_currency_long(self, mock_get_new_account):
        """
        Тест на создание кошелька с неверной валютой (длинное название)
        """

        data = {'currency': self.fake_currency_name_long}

        response = self.client.post(self.wallets_url, data, format='json')

        # Проверяем, что метод get_new_account не был вызван
        mock_get_new_account.assert_not_called()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        content = json.loads(response.content.decode())
        self.assertEqual(content['currency'], ['Убедитесь, что это значение содержит не более 3 символов.'])

    @patch.object(CryptoManager, 'get_balances')
    def test_list_wallets_with_balance(self, mock_get_balances):
        """
        Тест на получение списка кошельков с балансом
        """

        # Создаем два кошелька
        wallet1 = Wallet.objects.create(currency=self.currency_names[0], public_key='test_public_key_1',
                                        private_key='test_private_key_1')
        wallet2 = Wallet.objects.create(currency=self.currency_names[0], public_key='test_public_key_2',
                                        private_key='test_private_key_2')

        # Замокаем метод get_balances
        mock_get_balances.return_value = [
            {'address': 'test_public_key_1', 'balance': 1},
            {'address': 'test_public_key_2', 'balance': 2},
        ]

        response = self.client.get(self.wallets_url, format='json')

        # Проверяем, что был вызван метод get_balances
        mock_get_balances.assert_called_once_with(['test_public_key_1', 'test_public_key_2'])

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = [
            {'id': wallet1.id, 'currency': self.currency_names[0], 'public_key': 'test_public_key_1', 'balance': 1},
            {'id': wallet2.id, 'currency': self.currency_names[0], 'public_key': 'test_public_key_2', 'balance': 2},
        ]

        self.assertEqual(response.data, expected_data)

    @patch.object(CryptoManager, 'make_transaction')
    def test_make_transaction_success(self, mock_make_transaction):
        """
        Тест на успешное создание транзакции
        """
        # Замокаем метод make_transaction
        mock_make_transaction.return_value = 'test_transaction_hash'

        wallet1 = Wallet.objects.create(
            currency=self.currency_names[0],
            public_key='test_public_key1',
            private_key='test_private_key1',
        )

        wallet2 = Wallet.objects.create(
            currency=self.currency_names[0],
            public_key='test_public_key2',
            private_key='test_private_key2',
        )

        # Создаем данные для запроса
        data = {
            'from': wallet1.public_key,
            'to': wallet2.public_key,
            'amount': 1,
            'currency': self.currency_names[0],
        }
        response = self.client.post(self.transaction_url, data, format='json')

        # Проверяем, что метод make_transaction был вызван
        mock_make_transaction.assert_called_once_with(
            from_address=wallet1.public_key,
            to_address=wallet2.public_key,
            amount=1,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'hash': 'test_transaction_hash'})

    @patch.object(CryptoManager, 'make_transaction')
    def test_make_transaction_to_absent_address(self, mock_make_transaction):
        """
        Тест на создание транзакции на адрес, которого нет в кошельке
        """
        # Замокаем метод make_transaction
        mock_make_transaction.side_effect = ValueError('Переводить можно только между кошельками внутри системы')

        # Создаем данные для запроса

        wallet = Wallet.objects.create(
            currency=self.currency_names[0],
            public_key='test_public_key',
            private_key='test_private_key',
        )

        addresses = [wallet.public_key, 'nonexistent_address_on_db']

        for address in addresses:
            # Проверяем что оба адреса должны быть в базе, проверяем как отправителя так и получателя
            data = {
                'from': address,
                'to': addresses[(addresses.index(address) - 1) % len(addresses)],
                'amount': 1,
                'currency': self.currency_names[0],
            }

            response = self.client.post(self.transaction_url, data, format='json')

            # Проверяем, что метод make_transaction не был вызван
            mock_make_transaction.assert_not_called()

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(response.data, {'from': ['Нельзя отправлять транзакцию между кошельками вне системы']})
