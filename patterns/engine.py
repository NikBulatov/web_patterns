from threading import local
from quopri import decodestring
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

    def find_category_by_id(self, id_: int) -> Category:
        for item in self.categories:
            print("item", item.id)
            if item.id == id_:
                return item
        raise Exception(f"No category with id = {id_}")

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


class UnitOfWork:
    current = local()

    def __init__(self):
        self.new_objects = []
        self.dirty_objects = []
        self.removed_objects = []

    def set_mapper_registry(self, mapper_registry):
        self.mapper_registry = mapper_registry

    def register_new(self, obj):
        self.new_objects.append(obj)

    def register_dirty(self, obj):
        self.dirty_objects.append(obj)

    def register_removed(self, obj):
        self.removed_objects.append(obj)

    def commit(self):
        self.insert_new()
        self.update_dirty()
        self.delete_removed()

        self.new_objects.clear()
        self.dirty_objects.clear()
        self.removed_objects.clear()

    def insert_new(self):
        print(self.new_objects)
        for obj in self.new_objects:
            print(f"Output {self.mapper_registry}")
            self.mapper_registry.get_mapper(obj).insert(obj)

    def update_dirty(self):
        for obj in self.dirty_objects:
            self.mapper_registry.get_mapper(obj).update(obj)

    def delete_removed(self):
        for obj in self.removed_objects:
            self.mapper_registry.get_mapper(obj).delete(obj)

    @classmethod
    def set_current(cls, unit_of_work):
        cls.current.unit_of_work = unit_of_work

    @staticmethod
    def new_current():
        __class__.set_current(UnitOfWork())

    @classmethod
    def get_current(cls):
        return cls.current.unit_of_work


class DomainObject:
    def mark_new(self):
        UnitOfWork.get_current().register_new(self)

    def mark_dirty(self):
        UnitOfWork.get_current().register_dirty(self)

    def mark_removed(self):
        UnitOfWork.get_current().register_removed(self)
