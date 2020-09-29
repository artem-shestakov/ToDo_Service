from itsdangerous import URLSafeTimedSerializer
from flask import current_app


def generate_verification_token(email):
    """Generate verification token for confirm user's email
    ":param email: User's email address"""
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])


def confirm_verification_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token,
                             max_age=expiration,
                             salt=current_app.config['SECURITY_PASSWORD_SALT'])
    except Exception as ex:
        return ex
    return email
