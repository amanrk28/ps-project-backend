import json

from rest_framework.renderers import BaseRenderer
from rest_framework.utils import json


class ApiRenderer(BaseRenderer):
    media_type = 'application/json'
    format = 'json'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response_dict = {
            'status': True,
            'data': {},
            'msg': '',
        }

        if data is None:
            response_dict['data'] = None
        else:
            if 'data' in data:
                response_dict['data'] = data['data']
            else:
                response_dict['data'] = data

            if 'msg' in data:
                response_dict['msg'] = data['msg']

            if 'status' in data and isinstance(data['status'], bool):
                response_dict['status'] = data['status']

        return json.dumps(response_dict)
