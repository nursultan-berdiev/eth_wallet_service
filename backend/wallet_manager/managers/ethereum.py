import asyncio
from typing import List

from django.conf import settings
from web3 import Web3, AsyncWeb3, AsyncHTTPProvider

from .abs_manager import AbsManager


class EthereumManager(AbsManager):
    """
    Менеджер для работы с Ethereum
    """
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.url = settings.ETH_NODE_URL + api_key
        self.web3async = AsyncWeb3(AsyncHTTPProvider(self.url))
        self.web3 = Web3(Web3.HTTPProvider(self.url))
        self.gas = 2000000

    async def _get_balance_async(self, address: str) -> dict:
        """
        Асинхронный метод для получения баланса по публичному ключу
        :param address: str
        :return: dict
        """
        return {'address': address, 'balance': await self.web3async.eth.get_balance(address)}

    async def _get_balances_async(self, addresses: List[str]) -> List[dict]:
        """
        Асинхронный метод для получения балансов по публичным ключам предоставленным в списке
        :param addresses: List[str]
        :return: List[dict]
        """
        tasks = [asyncio.create_task(self._get_balance_async(address)) for address in addresses]
        return [result for result in await asyncio.gather(*tasks)]

    def get_balances(self, addresses: List[str]) -> List[dict]:
        """
        Метод для получения балансов по публичным ключам предоставленным в списке
        :param addresses: List[str]
        :return: dict
        """
        return asyncio.run(self._get_balances_async(addresses))

    def get_balance(self, address: str) -> int:
        """
        Метод для получения баланса по публичному ключу
        :param address: str
        :return: balance: int
        """
        return self.web3.eth.get_balance(address)

    def get_accounts(self):
        """
        Метод для получения списка аккаунтов
        :return: List[str]
        """
        return self.web3.eth.accounts

    def get_new_account(self):
        """
        Метод для создания нового аккаунта
        :return: dict
        """
        account = self.web3.eth.account.create()
        return {
            'private_key': account.key.hex(),
            'public_key': account.address,
        }

    def make_transaction(self, from_address: str, to_address: str, amount: int) -> str:
        """
        Метод для создания транзакции
        :param from_address: str
        :param to_address: str
        :param amount: int
        :return: str
        """
        # сумма перевода должна быть больше чем баланс ĸошельĸа (плюс затраты на ĸомиссию сети — газ)
        if self.get_balance(from_address) < amount + self.gas * self.web3.eth.gas_price:
            raise ValueError('Сумма перевода должна быть больше, чем баланс кошелька')

        transaction = {
            'from': from_address,
            'to': to_address,
            'value': amount,
            'gas': self.gas,
            'gasPrice': self.web3.eth.gas_price,
            'nonce': self.web3.eth.get_transaction_count(from_address)
        }
        signed = self.web3.eth.account.send_transaction(transaction)
        return signed.hex()

    def connected(self) -> bool:
        """
        Метод для проверки подключения к ноде
        :return: bool
        """
        return self.web3.is_connected()
