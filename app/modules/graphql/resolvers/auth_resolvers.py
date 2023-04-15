from ..utils import return_validation_error
from ...models.users import Client
from ...models.tokens import TokenType
from ...db_gateways.users_gateway import UsersGateway
from ...session.session import get_session


def resolve_login(*_, login: str, password: str):
    with get_session() as db:
        try:
            user = UsersGateway.authenticate_user(login, password, db)
        except ValueError as validation_error:
            return return_validation_error(validation_error)

        access_token, refresh_token = UsersGateway.generate_auth_tokens(user.id)

        return {
            'tokens': {
                'access_token': access_token,
                'refresh_token': refresh_token,
            },
            'status': {
                'success': True,
            }
        }


def resolve_sing_up(*_, input: dict):
    with get_session() as db:
        try:
            user, token = UsersGateway.register_user(Client(**input), db)
        except ValueError as validation_error:
            return return_validation_error(validation_error)
        return {'user': user, 'token': token, 'status': {
            'success': True,
        }}


def resolve_account_confirm(*_, token: str):
    with get_session() as db:
        register_token = UsersGateway.check_token(token, TokenType.register, db)
        if register_token is None:
            return {'status': {
                'success': False,
                'error': 'Не найден активный токен с таким значением'
            }}
        UsersGateway.confirm_account(register_token, db)
        return {'user': register_token.user, 'status': {
            'success': True,
        }}


def resolve_request_reset(*_, email: str):
    with get_session() as db:
        try:
            user, token = UsersGateway.request_reset(email, db)
        except ValueError as validation_error:
            return return_validation_error(validation_error)
        return {'user': user, 'token': token, 'status': {
            'success': True,
        }}


def resolve_reset_confirm(*_, token: str, password: str):
    with get_session() as db:
        reset_token = UsersGateway.check_token(token, TokenType.reset, db)
        if reset_token is None:
            return {'status': {
                'success': False,
                'error': 'Не найден активный токен с таким значением'
            }}
        UsersGateway.confirm_reset(reset_token, password, db)
        return {'user': reset_token.user, 'status': {
            'success': True,
        }}


def resolve_refresh(*_, refresh_token: str):
    with get_session() as db:
        try:
            access_token, refresh_token = UsersGateway.refresh_auth_tokens(refresh_token, db)
        except ValueError as token_error:
            return {'status': {
                'success': False,
                'error': str(token_error),
            }}

        return {
            'tokens': {
                'access_token': access_token,
                'refresh_token': refresh_token,
            },
            'status': {
                'success': True,
            }
        }
