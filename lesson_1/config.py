from pydantic import BaseConfig


class MainConfig(BaseConfig):
    SECRET_KEY: str
    DEBUG: bool

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"
        env_prefix = ""


class Production(MainConfig):
    pass


class Development(MainConfig):
    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"
        env_prefix = "DEV_"


# class Testing(MainConfig):
#     class Config:
#         env_file = "../.env"
#         env_file_encoding = "utf-8"
#         env_prefix = "TEST_"
