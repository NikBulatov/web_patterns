from pydantic_settings import BaseSettings


class MainConfig(BaseSettings):
    SECRET_KEY: str
    DEBUG: bool
    TEMPLATES_PATH: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = ""


class Production(MainConfig):
    pass


class Development(MainConfig):
    pass

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "DEV_"


# class Testing(MainConfig):
#     class Config:
#         env_file = "../.env"
#         env_file_encoding = "utf-8"
#         env_prefix = "TEST_"

DEV_CONFIG = Development()
