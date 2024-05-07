from utils import token_generator


def generate_user_token(user):
    auth_token = token_generator.generate_auth_token(user)
    return auth_token
