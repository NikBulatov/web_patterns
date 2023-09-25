from quopri import decodestring
from time import time
from jsonpickle import encode, decode

from patterns.users import UserFactory, Student, User, Teacher
from patterns.categories import Category
from patterns.courses import CourseFactory, Course


class Engine:
    def __init__(self):
        self.teachers: list[Teacher] = []
        self.students: list[Student] = []
        self.courses: list[Course] = []
        self.categories: list[Category] = []

    @staticmethod
    def create_user(type_, name) -> User:
        return UserFactory.create(type_, name)

    @staticmethod
    def create_category(name, category=None) -> Category:
        return Category(name, category)

    def find_category_by_id(self, id: int) -> Category:
        for item in self.categories:
            print("item", item.id)
            if item.id == id:
                return item
        raise Exception(f"No category with id = {id}")

    @staticmethod
    def create_course(type_, name, category) -> Course:
        return CourseFactory.create(type_, name, category)

    def get_course(self, name) -> Course | None:
        for item in self.courses:
            if item.name == name:
                return item
        return None

    def get_student(self, name) -> Student:
        for item in self.students:
            if item.name == name:
                return item

    @staticmethod
    def decode_value(value) -> str:
        val_b = bytes(value.replace("%", "=").replace("+", " "), "UTF-8")
        val_decode_str = decodestring(val_b)
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


class Debug:
    def __init__(self, name):
        self.name = name

    def __call__(self, cls):
        def timeit(method):
            def timed(*args, **kw):
                ts = time()
                result = method(*args, **kw)
                te = time()
                delta = te - ts

                print(f"debug --> {self.name} executed {delta:2.2f} ms")
                return result

            return timed

        return timeit(cls)


class Route:
    def __init__(self, routes, path):
        self.routes = routes
        self.url = path

    def __call__(self, view):
        self.routes[self.url] = view()


class Observer:
    def update(self, subject):
        pass


class Subject:
    def __init__(self):
        self.observers = []

    def notify(self):
        for item in self.observers:
            item.update(self)


class SMSNotifier(Observer):
    def update(self, subject):
        print(f"SMS-> {subject.students[-1].name} was joined")


class EmailNotifier(Observer):
    def update(self, subject):
        print(f"EMAIL-> {subject.students[-1].name} was joined")


class BaseSerializer:
    def __init__(self, obj):
        self.obj = obj

    def save(self):
        return encode(self.obj)

    @staticmethod
    def load(data):
        return decode(data)


class ConsoleWriter:
    @staticmethod
    def write(text):
        print(text)


class FileWriter:
    def __init__(self):
        self.file_name = "log"

    def write(self, text):
        with open(self.file_name, "a", encoding="utf-8") as f:
            f.write(f"{text}\n")
