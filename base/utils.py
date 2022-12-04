import jwt as JWT
import environ

env = environ.Env()
environ.Env.read_env()


def jwt_decode(token):
    # slicing the authorization header to get jwt with "Bearer "
    jwt = token[7:]
    payload = JWT.decode(jwt, env("JWT_SECRET_KEY"), env("JWT_ALGORITHM"))
    return payload["user_id"]


delete_success = {"detail": "Deleted successfully"}
