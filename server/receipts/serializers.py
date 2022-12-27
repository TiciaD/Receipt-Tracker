from rest_framework import serializers

from .models import Receipt, Tag
from django.contrib.auth.models import User

from django.contrib.auth import password_validation
from django.contrib.auth.hashers import make_password
from rest_framework.validators import UniqueValidator


class TagSerializer(serializers.ModelSerializer):
    # receipts = serializers.PrimaryKeyRelatedField(
    #     many=True,
    #     queryset=Receipt.objects.all()
    # )
    # receipts = serializers.PrimaryKeyRelatedField(
    #     many=True,
    #     queryset=Receipt.objects.all()
    #     # read_only=True,
    #     # view_name='receipt-detail'
    # )

    class Meta:
        model = Tag
        fields = ('id', 'tag_name')


class ReceiptSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(
        read_only=True
        # view_name='user-detail', read_only=True
    )
    tags = serializers.SlugRelatedField(
        queryset=Tag.objects.all(),
        slug_field='tag_name',
        many=True
    )

    class Meta:
        model = Receipt
        fields = ['id', 'user', 'title', 'date', 'receipt_image', 'tags']


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, help_text=password_validation.password_validators_help_text_html())
    email = serializers.EmailField(required=True, validators=[
                                   UniqueValidator(queryset=User.objects.all())])
    # receipts = serializers.PrimaryKeyRelatedField(
    #     many=True,
    #     queryset=Receipt.objects.all(),
    #     required=False
    # )
    receipts = ReceiptSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'receipts']

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
        # user = self.context['request'].user
        # password_validation.validate_password(password=password, user=user)
        password_validation.validate_password(password)

        # return password
        return make_password(password)


class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, help_text=password_validation.password_validators_help_text_html())
    email = serializers.EmailField(required=True, validators=[
                                   UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def validate_password(self, password):
        password_validation.validate_password(password)

        return make_password(password)
