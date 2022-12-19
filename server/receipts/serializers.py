from rest_framework import serializers
from rest_framework.fields import CharField

from .models import User, Receipt, Tag
from django.contrib.auth.models import User

from django.contrib.auth import password_validation
from django.contrib.auth.hashers import make_password
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.HyperlinkedModelSerializer):
    receipts = serializers.HyperlinkedRelatedField(
        many=True, view_name='receipt-detail', read_only=True)
    email = serializers.EmailField(required=True, validators=[
                                   UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(
        help_text=password_validation.password_validators_help_text_html(), write_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'email', 'password', 'receipts')

    def validate_password(self, password):
        user = self.context['request'].user
        password_validation.validate_password(password=password, user=user)

        return make_password(password)


class ReceiptSerializer(serializers.HyperlinkedModelSerializer):
    creatorUrl = serializers.ReadOnlyField(source='creator.url')
    creator = serializers.ReadOnlyField(source='creator.username')
    tags = serializers.HyperlinkedRelatedField(
        many=True, view_name='tag-detail', queryset=Tag.objects.all())

    class Meta:
        model = Receipt
        fields = ('url', 'id', 'title', 'date',
                  'receiptImage', 'tags', 'creatorUrl', 'creator')


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ('url', 'id', 'tag', 'receipts')
