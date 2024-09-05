from typing import TypeVar, List

import base64

from models.user import User

from api.v1.auth.auth import Auth





class BasicAuth(Auth):

    def extract_base64_authorization_header(

        self, authorization_header: str

    ) -> str:

        if authorization_header is None or not isinstance(

                authorization_header, str):

            return None

        if not authorization_header.startswith('Basic '):

            return None

        return authorization_header[6:]



    def decode_base64_authorization_header(

        self, base64_authorization_header: str

    ) -> str:

        if base64_authorization_header is None or not isinstance(

                base64_authorization_header, str):

            return None

        try:

            decoded_bytes = base64.b64decode(base64_authorization_header)

            return decoded_bytes.decode('utf-8')

        except Exception:

            return None



    def extract_user_credentials(

        self, decoded_base64_authorization_header: str

    ) -> (str, str):

        if decoded_base64_authorization_header is None or not isinstance(

                decoded_base64_authorization_header, str):

            return None, None

        if ':' not in decoded_base64_authorization_header:

            return None, None

        return tuple(decoded_base64_authorization_header.split(':', 1))



    def user_object_from_credentials(

        self, user_email: str, user_pwd: str

    ) -> TypeVar('User'):

        if user_email is None or not isinstance(user_email, str):

            return None

        if user_pwd is None or not isinstance(user_pwd, str):

            return None

        user_list = User.search({'email': user_email})

        if not user_list:

            return None

        user = user_list[0]

        if not user.is_valid_password(user_pwd):

            return None

        return user



    def current_user(self, request=None) -> TypeVar('User'):

        if request is None:

            return None

        auth_header = self.authorization_header(request)

        if auth_header is None:

            return None

        base64_auth = self.extract_base64_authorization_header(auth_header)

        if base64_auth is None:

            return None

        decoded_auth = self.decode_base64_authorization_header(base64_auth)

        if decoded_auth is None:

            return None

        user_email, user_pwd = self.extract_user_credentials(decoded_auth)

        if user_email is None or user_pwd is None:

            return None

        user = self.user_object_from_credentials(user_email, user_pwd)

        return user
