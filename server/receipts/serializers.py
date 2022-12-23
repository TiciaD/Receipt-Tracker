from rest_framework import serializers

from .models import Receipt, Tag
from django.contrib.auth.models import User

from django.contrib.auth import password_validation
from django.contrib.auth.hashers import make_password
from rest_framework.validators import UniqueValidator


class TagSerializer(serializers.HyperlinkedModelSerializer):
    receipts = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='receipt-detail'
    )

    class Meta:
        model = Tag
        fields = ('url', 'id', 'tagName', 'receipts')


class ReceiptSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        view_name='user-detail', read_only=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = Receipt
        fields = ['url', 'id', 'user', 'title', 'date', 'receiptImage', 'tags']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(
        write_only=True, help_text=password_validation.password_validators_help_text_html())
    email = serializers.EmailField(required=True, validators=[
                                   UniqueValidator(queryset=User.objects.all())])
    receipts = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='receipt-detail'
    )

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'email', 'password', 'receipts']


    # def create(self, validated_data):
    #     password = validated_data.pop('password')
    #     user = User.objects.create(**validated_data)
    #     self.validate_password(password)
    #     user.set_password(password)
    #     user.save()
    #     return user

    # def update(self, instance, validated_data):
    #     instance.email = validated_data.get('email', instance.email)
    #     instance.username = validated_data.get('username', instance.username)

    #     password = validated_data.get('password')
    #     if password:
    #         self.validate_password(password)
    #         instance.set_password(password)

    #     instance.save()
    #     return instance

    def validate_password(self, password):
        user = self.context['request'].user
        password_validation.validate_password(password=password, user=user)

        return make_password(password)
