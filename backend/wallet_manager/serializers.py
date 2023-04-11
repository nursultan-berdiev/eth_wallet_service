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
        if attrs['from_address'] == attrs['to']:
            raise serializers.ValidationError('Нельзя отправлять транзакцию самому себе')
        return attrs

    def get_fields(self):
        """
        Переопределяем метод, чтобы переименовать поле from_address в from
        :return: fields: dict
        """
        fields = super().get_fields()
        fields['from'] = fields.pop('from_address')
        return fields

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
