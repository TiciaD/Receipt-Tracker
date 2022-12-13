from rest_framework import serializers
from rest_framework.fields import CharField

from .models import User, Receipt, Tag


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'id', 'email', 'password')

        read_only_fields = ('id',)
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8, 'max_length': 64}}


class ReceiptSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Receipt
        fields = ('url', 'id', 'date', 'image', 'user')

class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ('url', 'id', 'tag', 'receipts')
