from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from services.abstractapi import is_email_deliverable
from apps.users.constants import INVALID_EXISTING_PASSWORD_ERR_MSG, EMAIL_NOT_DELIVERABLE_ERR_MSG


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate_email(self, value):
        if is_email_deliverable(value):
            return value
        raise serializers.ValidationError(EMAIL_NOT_DELIVERABLE_ERR_MSG)

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            last_name=validated_data['last_name'],
            first_name=validated_data['first_name']
        )
        user.set_password(validated_data['password'])
        user.save(update_fields=['password'])
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'is_active')
        read_only_fields = ['id']


class UpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

    def validate_old_password(self, value):
        if not self.instance.check_password(value):
            raise serializers.ValidationError(INVALID_EXISTING_PASSWORD_ERR_MSG)
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save(update_fields=['password'])
        return instance

    @property
    def data(self):
        return 'Password Updated Successfully!'
