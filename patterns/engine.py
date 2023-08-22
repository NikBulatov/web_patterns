from base64 import decodebytes

from patterns.models import Model
from patterns.simples import Technique, Level
from patterns.users import UserFactory, User, Student, Teacher, Staff
from patterns.categories import Category
from patterns.courses import CourseFactory, CoursePrototype


class Engine:
    def __init__(self):
        self.teachers: list[Teacher] = []
        self.students: list[Student] = []
        self.staff: list[Staff] = []
        self.courses: list[CoursePrototype] = []
        self.categories: list[Category] = []
        self.models: list[Model] = []

    @staticmethod
    def create_user(type_: str) -> User:
        return UserFactory.create(type_)

    @staticmethod
    def create_category(name: str, category=None) -> Category:
        return Category(name, category)

    def find_category_by_id(self, id_: int) -> Category:
        for item in self.categories:
            print("item", item.id)
            if item.id == id_:
                return item
        raise Exception(f"NO category with ID {id_}")

    @staticmethod
    def create_course(
        type_, name: str, category: Category, models: list[Model]
    ) -> CoursePrototype:
        return CourseFactory.create(type_, name, category, models)

    @staticmethod
    def create_model(
        name: str,
        level: Level = Level.JUNIOR,
        technique: Technique = Technique.TRADITIONAL,
    ) -> Model:
        return Model(name, level, technique)

    def get_model(self, name: str) -> Model | None:
        for model in self.models:
            if model.name == name:
                return model
        return None

    def get_course(self, name: str) -> CoursePrototype | None:
        for course in self.courses:
            if course.name == name:
                return course
        return None

    @staticmethod
    def decode_value(value: str) -> str:
        val_b = bytes(value.replace("%", "=").replace("+", " "), "UTF-8")
        val_decode_str = decodebytes(val_b)
        return val_decode_str.decode("UTF-8")


class SingletonLogger(type):
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


class Logger(metaclass=SingletonLogger):
    def __init__(self, name: str):
        self.name = name

    @staticmethod
    def log(text: str) -> None:
        print("LOG --->", text)
