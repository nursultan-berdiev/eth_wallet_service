from django.conf import settings
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from drf_spectacular.utils import extend_schema

from .managers import CryptoManager
from .models import Wallet
from .serializers import WalletSerializer, WalletTransactionSerializer


class WalletView(ListCreateAPIView):
    """
    Класс для работы с кошельками
    """
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    pagination_class = LimitOffsetPagination

    @staticmethod
    def get_serializer_data_with_balance(serializer: Serializer) -> dict:
        """
        Метод для получения данных сериализатора с балансами, используя менеджеры
        :param serializer: Serializer
        :return: serializer.data: dict
        """

        # Получаем список публичных ключей для каждой валюты
        addresses_by_currency = {}
        for item in serializer.data:
            currency = item['currency']
            if currency not in addresses_by_currency:
                addresses_by_currency[currency] = []
            addresses_by_currency[currency].append(item['public_key'])

        # Получаем балансы для каждой валюты, используя соответствующий менеджер
        for currency, addresses in addresses_by_currency.items():
            manager = CryptoManager(settings.ETH_API_KEY, currency)
            balances = manager.get_balances(addresses)
            for balance in balances:
                for item in serializer.data:
                    if item['public_key'] == balance['address']:
                        item['balance'] = balance['balance']
                        break

        return serializer.data

    def list(self, request, *args, **kwargs):

        # Стандартная реализация не подходит, т.к. нам нужно получить балансы для каждого кошелька
        # и добавить их в ответ. Поэтому мы переопределяем метод list и дополняем данные в ответе
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)

            # Добавляем балансы в ответ
            return self.get_paginated_response(self.get_serializer_data_with_balance(serializer))

        serializer = self.get_serializer(queryset, many=True)

        # Добавляем балансы в ответ
        return Response(self.get_serializer_data_with_balance(serializer))

    def create(self, request, *args, **kwargs):
        # Стандартная реализация не подходит, т.к. нам нужно создать кошелек для каждой валюты

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Получаем валюту после проверки на валидность (чтобы не было ошибки при создании кошелька)
        currency = serializer.validated_data['currency']

        try:
            manager = CryptoManager(settings.ETH_API_KEY, currency)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Если валюта поддерживается, то создаем кошелек
        account = manager.get_new_account()
        # Сохраняем данные в базу
        serializer.save(**account)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class WalletTransactionCreateView(APIView):
    """
    Класс для создания транзакций
    """
    serializer_class = WalletTransactionSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            manager = CryptoManager(settings.ETH_API_KEY, serializer.validated_data['currency'])
            hash_transaction = manager.make_transaction(
                from_address=serializer.validated_data['from'],
                to_address=serializer.validated_data['to'],
                amount=serializer.validated_data['amount']
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'hash': hash_transaction}, status=status.HTTP_201_CREATED)
