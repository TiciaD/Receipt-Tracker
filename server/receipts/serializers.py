from rest_framework import serializers

from .models import Receipt, Tag
from django.contrib.auth.models import User

from django.contrib.auth import password_validation
from django.contrib.auth.hashers import make_password
from rest_framework.validators import UniqueValidator


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ('url', 'id', 'tagName')


class ReceiptSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Receipt
        fields = ['url', 'id' 'user', 'title', 'date', 'receiptImage', 'tags']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField()
    receipts = ReceiptSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['url', 'id' 'email', 'username', 'password', 'receipts']
        extra_kwargs = {
            'email': {
                'validators': [UniqueValidator(queryset=User.objects.all())],
                'required': True,
            },
            'password': {
                'write_only': True,
            },
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        password_validation.validate_password(password, user)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)

        password = validated_data.get('password')
        if password:
            password_validation.validate_password(password, instance)
            instance.set_password(password)

        instance.save()
        return instance

    # def validate_password(self, password):
    #     user = self.context['request'].user
    #     password_validation.validate_password(password=password, user=user)

    #     return make_password(password)
