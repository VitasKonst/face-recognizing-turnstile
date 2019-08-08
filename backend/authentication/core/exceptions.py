from rest_framework.views import exception_handler


def core_exception_handler(exc, context):
    # Если возникает исключение, которое мы здесь явно не обрабатываем, мы хотим,
    # поручить его обработку стандартному DRF обработчику. Если мы хотим обработать данный тип исключения,
    # то нам всё равно нужен доступ к ответу, генерируемому DRF,
    # поэтому в первую очередь необходимо получить его.
    response = exception_handler(exc, context)
    handlers = {
        'ValidationError': _handle_generic_error,
    }
    # В строке кода после этого комментария видно как мы определяем
    # тип текущего исключения. Затем мы используем его, чтобы понять должны ли мы обрабатывать это
    # исключение или можно позволить Django REST фреймворку сделать это за нас.
    exception_class = exc.__class__.__name__

    if exception_class in handlers:
        # Если это исключение одно из тех, что мы хотим обрабатывать, то обрабатываем его. В противном случае,
        # возвращаем ответ, сгенерированный ранее стандартным обработчиком исключений.
        return handlers[exception_class](exc, context, response)

    return response


def _handle_generic_error(exc, context, response):
    # Это самый простой обработчик исключений, который мы можем создать.
    # Мы просто получаем ответ, сгенерированный DRF и помещаем его в пространство имен `errors`.
    response.data = {
        'errors': response.data
    }

    return response
