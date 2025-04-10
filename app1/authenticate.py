from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed


class OneTokenPerUserAuthentication(JWTAuthentication):
    def authenticate(self, request):

        auth_result = super().authenticate(request)

        if auth_result is None:
            return None

        auth_user, token = auth_result

        payload = token.payload
        print(payload, 'payload...')
        login_time = payload.get('login_time')
        print(auth_user.last_login.timestamp(), 'auth user last llogin')
        print(login_time, 'login time')
        if login_time is None:
            raise AuthenticationFailed('Invalid token')

        if login_time != auth_user.last_login.timestamp():
            raise AuthenticationFailed('Oops, your season is expired')

        return auth_result


