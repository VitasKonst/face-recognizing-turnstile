import jwt
import os
import datetime
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from .managers import UserManager
from main.abonement_details import *
from .transliteration import KazakhLanguagePack
from transliterate import translit
from transliterate.discover import autodiscover
from transliterate.base import registry


def content_file_name(instance, filename):
    autodiscover()
    registry.register(KazakhLanguagePack)

    ext = filename.split('.')[-1]

    filename = "%s_%s_%s.%s" % (str(instance.pk), translit(instance.last_name, 'kz', reversed=True),
                                translit(instance.first_name, 'kz', reversed=True), ext)

    filename = filename.lower()

    return os.path.join('portraits', filename)


class User(AbstractBaseUser, PermissionsMixin):
    phone_regex = RegexValidator(regex=r'^\+77\d{9}$',
                                 message="Номер телефона должен быть введен в следующем формате: '+77123456789'",)

    GENDER_CHOICES = (
        ('М', 'Мужской'),
        ('Ж', 'Женский'),
    )

    required_field_warning = _('Необходимо заполнить это поле.')

    phone = models.CharField(
        _('номер телефона'),
        max_length=12,
        unique=True,
        help_text=required_field_warning,
        validators=[phone_regex, ],
        error_messages={
            'unique': _("Пользователь с таким номером телефона уже существует"),
        },
    )
    portrait = models.ImageField(_('фото'), upload_to=content_file_name)
    last_name = models.CharField(_('фамилия'), max_length=30, help_text=required_field_warning, )
    first_name = models.CharField(_('имя'), max_length=30, help_text=required_field_warning, )
    patronymic = models.CharField(_('отчество'), max_length=30, blank=True, )
    email = models.EmailField(_('адрес электронной почты'), blank=True, )
    gender = models.CharField(_('пол'), max_length=1, choices=GENDER_CHOICES, help_text=required_field_warning, )
    date_of_birth = models.DateField(_('дата рождения'), default=datetime.date.today, help_text=required_field_warning)
    date_joined = models.DateTimeField(_('дата регистрации'), auto_now_add=True, )
    national_id = models.CharField(
        _('номер удостоверения личности'),
        max_length=9,
        validators=[RegexValidator(regex=r'\d{9}',
                                   message='Ввведите 9-ти значный номемер удостоверени личности пользователя'), ],
        help_text=required_field_warning,
    )

    abonement_type = models.IntegerField(_('тип абонемента'), choices=ABONEMENT_TYPE_CHOICES,
                                         default=0, )
    abonement_registration_date = models.DateField(_('дата регистрации абонемента'), auto_now=True, )
    abonement_visits_left = models.IntegerField(_('посещений доступно'), choices=ABONEMENT_VISITS_CHOICES,
                                                help_text=required_field_warning, default=0)
    abonement_validity_period = models.IntegerField(_('период действия'), choices=ABONEMENT_PERIOD_CHOICES,
                                                    help_text=required_field_warning, default=0)

    is_active = models.BooleanField(_('activeness status'), default=True, )
    is_staff = models.BooleanField(_('staff status'), default=True, )

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone

    @property
    def token(self):
        return self._generate_jwt_token()

    class Meta:
        verbose_name = _('Клиент')
        verbose_name_plural = _('клиенты')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def get_absolute_url(self):
        return "/users/%i/" % self.pk

    def _generate_jwt_token(self):
        token = jwt.encode({
            'id': self.pk,
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

    def get_portrait(self):
        if self.portrait:
            return self.portrait

        return 'https://static.productionready.io/images/smiley-cyrus.jpg'


class Attendance(models.Model):
    PASSING_SIDE_CHOICES = (
        (0, 'Вход'),
        (1, 'Выход'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='клиент')
    date = models.DateTimeField(_('дата посещения'), default=datetime.datetime.now())
    side = models.IntegerField(_('направление'), choices=PASSING_SIDE_CHOICES, default=0)

    class Meta:
        ordering = ('date', )
        verbose_name = _('посещение')
        verbose_name_plural = _('посещения')
