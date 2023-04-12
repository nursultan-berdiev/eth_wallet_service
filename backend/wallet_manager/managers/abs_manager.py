from abc import ABC, abstractmethod
from typing import List


class AbsManager(ABC):
    """
    Абстрактный класс для работы с криптовалютами
    Все менеджеры должны наследоваться от этого класса и предоставлять реализацию всех методов
    """
    @abstractmethod
    def get_balance(self, address: str) -> int:
        """
        Абстрактный метод для получения баланса по публичному ключу
        :param address: str - Публичный ключ
        :return: balance: int - Баланс
        """
        pass

    @abstractmethod
    def get_balances(self, addresses: List[str]) -> List[dict]:
        """
        Абстрактный метод для получения списка балансов по публичным ключам
        :param addresses: List[str]
        :return: dict
        """
        pass

    @abstractmethod
    def get_accounts(self) -> List[str]:
        """
        Абстрактный метод для получения списка аккаунтов
        :return: List[str]
        """
        pass

    @abstractmethod
    def get_new_account(self) -> dict:
        """
        Абстрактный метод для получения нового аккаунта
        :return: dict
        """
        pass

    @abstractmethod
    def make_transaction(self, from_address: str, to_address: str, amount: int) -> str:
        """
        Абстрактный метод для создания транзакции
        :param from_address: str - Адрес отправителя
        :param to_address: str - Адрес получателя
        :param amount: int - Сумма перевода
        :return: hash: str - Хэш транзакции
        """
        pass

    @abstractmethod
    def connected(self) -> bool:
        """
        Абстрактный метод для проверки подключения к ноде
        :return: bool
        """
        pass
