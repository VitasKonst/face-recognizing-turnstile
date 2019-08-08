from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, AdminPasswordChangeForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from authentication.models import User


admin.site.site_header = 'Управление комплексом турникетов'


class UserCreationForm(forms.ModelForm):

    standard_password = 'MethodPro-2019'

    class Meta:
        model = User
        fields = ('password', )
        readonly_fields = ('password', )

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.standard_password)
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label="Пароль",
                                         help_text=("Пароли пользователей не хранятся вы чистом виде, поэтому "
                                                    "увидеть пароль этого пользователя невозможно, но вы все "
                                                    "ещё можете изменить его, используя "
                                                    "<a href=\"../password/\">эту форму</a>."))

    class Meta:
        model = User
        fields = ()

    def clean_password(self):
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    list_display = (
        'phone',
        'last_name',
        'first_name',
        'email',
        'is_superuser',)
    list_filter = ('is_superuser',)
    fieldsets = (
        (None, {'fields': ('phone', 'password',)}),
        ('Биометрические данные', {'fields': ('portrait', )}),
        ('Персональные данные', {'fields': ('last_name', 'first_name', 'patronymic', 'gender', 'email', 'date_of_birth', 'national_id', 'date_joined',)}),
        ('Информация об абонементе', {'fields': ('abonement_type', 'abonement_registration_date',
                                                 'abonement_validity_period', 'abonement_visits_left', )}),
        ('Разрешения', {'fields': ('is_superuser', )}),
    )

    readonly_fields = ('date_joined', 'abonement_registration_date', )

    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('phone',)}),
        ('Биометрические данные', {'classes': ('wide',), 'fields': ('portrait', )}),
        ('Персональные данные', {'classes': ('wide',), 'fields': ('last_name', 'first_name', 'patronymic', 'email',
                                                                  'gender', 'date_of_birth', 'national_id',)}),
        ('Информация об абонементе', {'classes': ('wide',), 'fields': ('abonement_type', 'abonement_validity_period',
                                                                       'abonement_visits_left', )}),
    )
    search_fields = ('phone_number',)
    ordering = ('date_joined',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
