import jwt
import environ

env = environ.Env()
environ.Env.read_env()


def jwt_decode(token):
    payload = jwt.decode(token, env("JWT_SECRET_KEY"), env("JWT_ALGORITHM"))
    return payload["user_id"]
