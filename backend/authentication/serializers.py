from django.conf import settings
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from .models import User


def authenticate(username=None, password=None, **kwargs):
    if username is None:
        username = kwargs.get(User.USERNAME_FIELD)
    try:
        user = User._default_manager.get_by_natural_key(username)
    except User.DoesNotExist:
        User().set_password(password)
    else:
        if user.check_password(password):
            return user
        else:
            return None


class LoginSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=255, write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ('phone', 'password', 'token', 'id')

    def validate(self, data):
        phone = data.get('phone', None)
        password = data.get('password', None)

        user = User.objects.model(phone=phone, password=password)
        user = authenticate(username=user.phone, password=user.password)

        if user is None:
            raise serializers.ValidationError(
                _('Данные указаны неверно')
            )

        if not user.is_active:
            raise serializers.ValidationError(
                _('Данный пользователь был деактивирован')
            )

        return {
            'id': user.id,
            'token': user.token
        }


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    date_joined = serializers.DateTimeField(format='%d.%m.%Y %H:%M', read_only=True)
    date_of_birth = serializers.DateField(format='%d.%m.%Y', input_formats=settings.DATE_INPUT_FORMATS)
    is_active = serializers.BooleanField(read_only=True)
    portrait = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ['is_superuser', 'is_staff', 'groups', 'user_permissions']
        read_only_fields = ('token', )

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance

    def get_portrait(self, obj):
        if obj.portrait:
            return obj.portrait.url

        return 'https://static.productionready.io/images/smiley-cyrus.jpg'


class AttendanceSerializer(serializers.ModelSerializer):
    time = serializers.DateTimeField(format='%d.%m.%Y %H:%M', read_only=True)
    side = serializers.IntegerField()
