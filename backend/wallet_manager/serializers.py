import copy

from rest_framework import serializers

from .models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    """
    Сериализатор для кошелька, используется для получения списка кошельков и создания нового
    """

    class Meta:
        model = Wallet
        fields = ('id', 'currency', 'public_key')
        read_only_fields = ('public_key',)


class WalletTransactionSerializer(serializers.Serializer):
    """
    Сериализатор для транзакции, используется для отправки транзакции
    """
    from_address = serializers.CharField(max_length=44, required=True, write_only=True)
    to = serializers.CharField(max_length=44, required=True, write_only=True)
    amount = serializers.DecimalField(max_digits=20, decimal_places=8, required=True, write_only=True)
    currency = serializers.CharField(max_length=3, required=True, write_only=True)
    hash = serializers.CharField(max_length=66, required=False, read_only=True)

    def validate(self, attrs):
        """
        Переопределяем метод, чтобы проверить, что адрес отправителя не совпадает с адресом получателя
        """
        # переводить можно тольĸо между ĸошельĸами внутри системы
        if not Wallet.objects.filter(public_key=attrs['from']).exists() or \
                not Wallet.objects.filter(public_key=attrs['to']).exists():
            raise serializers.ValidationError({'from': ['Нельзя отправлять транзакцию между кошельками вне системы']})

        if attrs['from'] == attrs['to']:
            raise serializers.ValidationError({'from': ['Нельзя отправлять транзакцию самому себе']})
        return attrs

    def get_fields(self):
        """
        Переопределяем метод, чтобы переименовать поле from_address в from
        """
        fields = copy.deepcopy(super().get_fields())
        fields['from'] = fields.pop('from_address')
        return fields

    def create(self, validated_data):
        """
        Должен быть переопределен, но не используется
        """
        pass

    def update(self, instance, validated_data):
        """
        Должен быть переопределен, но не используется
        """
        pass
