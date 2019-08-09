from .core.renderers import MyJSONRenderer


class UserJSONRenderer(MyJSONRenderer):
    header = 'user'

    def render(self, data, media_type=None, renderer_context=None):
        token = data.get('token', None)

        if token is not None and isinstance(token, bytes):
            data['token'] = token.decode('utf-8')

        return super().render(data=data, media_type=media_type, renderer_context=renderer_context)


class AttendanceJSONRenderer(MyJSONRenderer):
    header = 'attendance'

    def render(self, data, media_type=None, renderer_context=None):
        return super().render(data=data, media_type=media_type, renderer_context=renderer_context)
