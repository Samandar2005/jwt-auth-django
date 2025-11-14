from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile display and update.
    Excludes sensitive fields like password.
    """
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 
                  'phone', 'bio', 'avatar', 'birth_date', 'date_joined', 'last_login')
        read_only_fields = ('id', 'email', 'date_joined', 'last_login')
        extra_kwargs = {
            'phone': {'required': False},
            'bio': {'required': False},
            'avatar': {'required': False},
            'birth_date': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
        }


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'password2', 'first_name', 'last_name', 'phone', 'bio', 'avatar', 'birth_date')
        extra_kwargs = {
            'phone': {'required': False},
            'bio': {'required': False},
            'avatar': {'required': False},
            'birth_date': {'required': False}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializer for password change functionality.
    Validates old password and new password.
    """
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, value):
        """
        Check if the old password is correct.
        """
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def validate(self, attrs):
        """
        Check if new passwords match.
        """
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "New password fields didn't match."})
        return attrs

    def save(self):
        """
        Save the new password.
        """
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
