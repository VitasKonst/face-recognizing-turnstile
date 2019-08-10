from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.backends import JWTAuthentication
from authentication.models import User, Attendance
from .cv import do_portraits_match
from .camera import get_image_from_camera
from .abonement_details import is_abonement_valid
import main.turnstile as turnstile


class PassViewModel(APIView):
    backend = JWTAuthentication()

    def post(self, request):
        try:
            user = self.backend.authenticate(request)[0]
        except TypeError:
            return Response({
                'errors': {
                    'message': 'Ошибка доступа.'
                }
            })

        side = request.data.get('side', None)
        id = request.data.get('id', None)

        if id is None or side is None:
            return Response({
                'status': 'failure',
                'message': 'Not enough data provided'
            })

        if side == '0':
            photo1 = user.portrait.path
            photo2 = get_image_from_camera()

            if do_portraits_match(photo1, photo2):
                if is_abonement_valid(user):
                    turnstile.accept(id=id, side='entrance')
                    attendance = Attendance.objects.create(user=user, side=0)
                    date = attendance.date.strftime(format='%d.%m.%Y')
                    return Response({
                        'status': 'success',
                        'message': 'Вы можете войти',
                        'passing_date': date
                    })
                else:
                    turnstile.deny('abonement has expired')
                    return Response({
                        'status': 'failure',
                        'message': 'Ваш абонемент истек или более не действителен',
                    })
            else:
                turnstile.deny('your face was not recognized')
                return Response({
                    'status': 'failure',
                    'message': 'Ваше лицо было распознано неверно',
                })
        else:
            turnstile.accept(id=id, side='exit')
            attendance = Attendance.objects.create(user=user, side=1)
            date = attendance.date.strftime(format='%d.%m.%Y')
            return Response({
                'status': 'success',
                'message': 'Вы можете выйти',
                'passing_date': date,
            })


