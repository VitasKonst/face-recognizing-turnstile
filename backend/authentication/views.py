from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.backends import JWTAuthentication

from .serializers import LoginSerializer, UserSerializer
from .renderers import UserJSONRenderer


class LoginAPIView(APIView):
    permission_classes = (AllowAny, )
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer
    backend = JWTAuthentication()

    def retrieve(self, request, *args, **kwargs):
        try:
            user = self.backend.authenticate(request)[0]
        except TypeError:
            return Response({
                'errors': {
                    'message': 'Ошибка доступа.'
                }
            })

        if user.id is not self.kwargs.get('pk'):
            return Response({
                'errors': {
                    'message': 'Ошибка доступа.'
                }
            })

        serializer = self.serializer_class(user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        try:
            user = self.backend.authenticate(request)[0]
        except TypeError:
            return Response({
                'errors': {
                    'message': 'Ошибка доступа.'
                }
            })

        if user.id is not self.kwargs.get('pk'):
            return Response({
                'errors': {
                    'message': 'Ошибка доступа.'
                }
            })

        serializer_data = request.data.get('user', {})

        serializer = self.serializer_class(
            user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

