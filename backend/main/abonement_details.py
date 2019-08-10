from django.utils import timezone
from dateutil.relativedelta import relativedelta

ABONEMENT_TYPE_CHOICES = (
    (0, 'Абонемент недействителен'),
    (1, 'Абонемент на заданный период'),
    (2, 'Абонемент сотрудника'),
)

ABONEMENT_PERIOD_CHOICES = (
    (0, 'Не указан'),
    (1, '1 месяц'),
    (3, '3 месяца'),
    (6, '6 месяцев'),
    (12, '1 год'),
)


def is_abonement_valid(user):
    type = user.abonement_type
    if type is 0:
        return False
    elif type is 1:
        current_date = timezone.now().date()
        expiration_date = user.abonement_registration_date + relativedelta(months=user.abonement_validity_period)
        if not current_date < expiration_date:
            user.abonement_type = 0
            user.save()
            return False
        return True
    elif type is 2:
        return True
