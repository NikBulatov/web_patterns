# Origami courses
from copy import deepcopy
from categories import Category
from patterns.models import Model


class CoursePrototype:
    def clone(self):
        return deepcopy(self)


class Course(CoursePrototype):
    def __init__(self, name: str, category: Category, models: list[Model]):
        self.name = name
        self.category = category
        self.models = models
        self.category.courses.append(self)


class InteractiveCourse(Course):
    pass


class RecordedCourse(Course):
    pass


class CourseFactory:
    types = {"interactive": InteractiveCourse, "record": RecordedCourse}

    @classmethod
    def create(cls, type_: str, name: str, category: Category, models: list[Model]):
        return cls.types[type_](name, category, models)
