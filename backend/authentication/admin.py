from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from authentication.models import User, Attendance
from django.contrib.auth.models import Group


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

    list_display = (
        'phone',
        'last_name',
        'first_name',
        'email',
        'is_staff',)
    list_filter = ('is_staff',)
    fieldsets = (
        (None, {'fields': ('phone', 'password',)}),
        ('Биометрические данные', {'fields': ('portrait', )}),
        ('Персональные данные', {'fields': ('last_name', 'first_name', 'patronymic', 'gender', 'email', 'date_of_birth',
                                            'national_id', 'date_joined',)}),
        ('Информация об абонементе', {'fields': ('abonement_type', 'abonement_registration_date',
                                                 'abonement_validity_period', )}),
        ('Разрешения', {'fields': ('is_staff', )}),
    )

    readonly_fields = ('date_joined', 'abonement_registration_date', )

    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('phone',)}),
        ('Биометрические данные', {'classes': ('wide',), 'fields': ('portrait', )}),
        ('Персональные данные', {'classes': ('wide',), 'fields': ('last_name', 'first_name', 'patronymic', 'email',
                                                                  'gender', 'date_of_birth', 'national_id',)}),
        ('Информация об абонементе', {'classes': ('wide',), 'fields': ('abonement_type', 'abonement_validity_period')}),
        ('Разрешения', {'fields': ('is_staff', )}),
    )
    search_fields = ('phone_number',)
    ordering = ('date_joined',)
    filter_horizontal = ()


class AttendanceCreationForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ()

    def save(self, commit=True):
        obj = super(AttendanceCreationForm, self).save(commit=False)
        if commit:
            obj.save()
        return obj


class AttendanceChangeForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ()
        readonly_fields = ('date', )


class AttendanceAdmin(ModelAdmin):
    form = AttendanceChangeForm
    add_form = AttendanceCreationForm

    list_display = (
        'date',
        'user',
        'side',)
    list_filter = ('user',)
    fieldsets = (
        (None, {'fields': ('user', 'date', 'side')}),
    )

    add_fieldsets = (
        (None, {'fields': ('user', 'date', 'side')}),
    )
    search_fields = ('date',)
    ordering = ('date',)
    filter_horizontal = ()

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('user', 'date', 'side')
        return self.readonly_fields


admin.site.register(User, UserAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.unregister(Group)
