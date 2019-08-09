import json
from rest_framework.renderers import JSONRenderer


class MyJSONRenderer(JSONRenderer):
    charset = 'utf-8'
    header = 'data'

    def render(self, data, media_type=None, renderer_context=None):
        errors = data.get('errors', None)

        if errors is not None:
            return json.dumps(data)

        return json.dumps({
            self.header: data
        })
