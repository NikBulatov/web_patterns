from base64 import decodestring

from users import UserFactory
from categories import Category
from courses import CourseFactory


class Engine:
    def __init__(self):
        self.teachers: list = []
        self.students: list = []
        self.courses: list = []
        self.categories: list = []

    @staticmethod
    def create_user(type_: str):
        return UserFactory.create(type_)

    @staticmethod
    def create_category(name: str, category=None):
        return Category(name, category)

    def find_category_by_id(self, id_: int):
        for item in self.categories:
            print("item", item.id)
            if item.id == id_:
                return item
        raise Exception(f"NO category with ID {id_}")

    @staticmethod
    def create_course(type_, name: str, category: Category):
        return CourseFactory.create(type_, name, category)

    def get_course(self, name):
        for item in self.courses:
            if item.name == name:
                return item
        return None

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace("%", "=").replace("+", " "), "UTF-8")
        val_decode_str = decodestring(val_b)
        return val_decode_str.decode("UTF-8")


class Singleton(type):
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs["name"]

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=Singleton):
    def __init__(self, name):
        self.name = name

    @staticmethod
    def log(text):
        print("log--->", text)
