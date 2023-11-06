import re
from rest_framework import serializers
from rest_framework.exceptions import ParseError, ValidationError
from django.contrib.auth.hashers import make_password

from .models import User


class SignupSerializer(serializers.ModelSerializer):
    user_lat = serializers.FloatField(write_only=True, required=False)
    user_lon = serializers.FloatField(write_only=True, required=False)

    class Meta:
        model = User
        fields = (
            "pk",
            "username",
            "email",
            "password",
            "user_lat",
            "user_lon",
        )

    def create(self, validated_data):
        password = validated_data.pop("password")
        # user_lat = validated_data.pop("user_lat", default=0.0)
        # user_lon = validated_data.pop("user_lon", default=0.0)
        hashed_password = make_password(password)
        user = User.objects.create(
            password=hashed_password,
            # user_lat=user_lat,
            # user_lon=user_lon,
            **validated_data,
        )
        return user

    def validate_password(self, password):
        if password:
            if not re.search(r"[a-z,A-Z]", password):
                raise ValidationError("비밀번호는 영문을 포함해야 합니다.")
            if not re.search(r"[0-9]", password):
                raise ValidationError("비밀번호는 숫자를 포함해야 합니다.")
            if len(password) < 8 or len(password) > 16:
                raise ValidationError("비밀번호는 8자 이상 16자 이하이어야 합니다.")
            print(password)
        else:
            raise ParseError("비밀번호를 입력하세요.")
        return password

      
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "pk",
            "username",
        )
        read_only_fields = ("pk",)


class MyPageSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        # fields = "__all__"
        read_only_fields = ("pk",)
        exclude = ("is_superuser", "is_staff", "is_admin", "groups", "user_permissions")
