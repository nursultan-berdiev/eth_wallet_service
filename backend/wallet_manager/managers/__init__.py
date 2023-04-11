from typing import List

from .abs_manager import AbsManager
from .ethereum import EthereumManager

CURRENCY_MANAGERS = {
    'ETH': EthereumManager,
}


class CryptoManagerError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class CryptoManager:
    """
    Класс для работы с криптовалютами
    """

    def __init__(self, api_key: str, currency: str):
        self.currency = currency

        # Проверяем, что валюта поддерживается
        if currency not in CURRENCY_MANAGERS:
            raise CryptoManagerError(f'Валюта {currency} не поддерживается')

        self.manager = CURRENCY_MANAGERS[currency](api_key)

        # Проверяем, что менеджер валюты является наследником AbsManager
        if not isinstance(self.manager, AbsManager):
            raise CryptoManagerError(f'Менеджер валюты {currency} не является наследником AbsManager')

    def get_balance(self, address: str) -> int:
        """
        Получение баланса по публичному ключу
        :param address: str - Публичный ключ
        :return: balance: int - Баланс
        """
        return self.manager.get_balance(address)

    def get_balances(self, addresses: List[str]) -> List[dict]:
        """
        Получение балансов по публичным ключам
        :param addresses: List[str] - Публичные ключи
        :return: balances: List[dict] - Балансы
        """
        return self.manager.get_balances(addresses)

    def get_accounts(self):
        """
        Получение списка аккаунтов
        :return: accounts: List[str] - Список аккаунтов
        """
        return self.manager.get_accounts()

    def get_new_account(self):
        """
        Получение нового аккаунта
        :return: account: dict - Новый аккаунт
        """
        return self.manager.get_new_account()

    def make_transaction(self, from_address: str, to_address: str, amount: int) -> str:
        """
        Создание транзакции
        :param from_address: str - Адрес отправителя
        :param to_address: str - Адрес получателя
        :param amount: int - Сумма перевода
        :return: hash: str - Хэш транзакции
        """
        return self.manager.make_transaction(from_address, to_address, amount)
