import secrets
import string
import datetime
from rest_framework import status, permissions
from rest_framework.response import Response as drf_response
from rest_framework.exceptions import APIException, PermissionDenied, AuthenticationFailed
from rest_framework.views import exception_handler

def compute_hash(hash_length=8):
    return ''.join(
        secrets.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(hash_length))

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    if isinstance(exc, AuthenticationFailed):
        response.data = {'msg': str(exc), 'status': False, 'data': None}
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return response
    if isinstance(exc, PermissionDenied):
        response.data = {'msg': str(exc), 'status': False, 'data': None}
        response.status_code = status.HTTP_403_FORBIDDEN
        return response
    elif isinstance(exc, APIException):
        data = None
        if hasattr(exc, 'data'):
            data = exc.data
        response.data = {'msg': str(exc), 'status': False, 'data': data}
        response.status_code = status.HTTP_200_OK
        return response
    else:
        return response

class Response(drf_response):
    def __init__(self, data=None, status=None, template_name=None, headers=None, exception=False, content_type=None,
                 msg=''):
        super().__init__(data=data, status=status, template_name=template_name, headers=headers, exception=exception,
                         content_type=content_type)
        self.data = {'data': data, 'msg': msg}

def permission_required(permission_names, raise_exception=False):
    class PermissionRequired(permissions.BasePermission):
        def has_permission(self, request, view):
            user = request.user
            if len(set(permission_names) & user.get_all_permissions()) > 0:
                return True
            if raise_exception:
                raise PermissionDenied()
            return False

    return PermissionRequired

def get_datetime_from_timestamp(time_in_ms):
    if isinstance(time_in_ms, str):
        timestamp = int(time_in_ms)
        dt_object = datetime.datetime.fromtimestamp(timestamp / 1000)
        return dt_object
    return time_in_ms