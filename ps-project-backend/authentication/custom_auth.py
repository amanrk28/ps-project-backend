from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

from authentication.models import AuthToken


class CustomTokenAuthentication(TokenAuthentication):
    model = AuthToken

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            auth_token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise AuthenticationFailed()

        if auth_token.deleted or not auth_token.user.is_active:
            raise AuthenticationFailed()

        return auth_token.user, auth_token