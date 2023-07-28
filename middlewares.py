from config import DEV_CONFIG


def secret_key(request: dict) -> None:
    """
    Add header "secret" in request headers
    :param request:
    :return:
    """
    request["secret"] = DEV_CONFIG.SECRET_KEY


middlewares = (secret_key,)
