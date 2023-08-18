# Origami courses
from copy import deepcopy
from categories import Category


class CoursePrototype:
    def clone(self):
        return deepcopy(self)


class Course(CoursePrototype):
    def __init__(
        self,
        name: str,
        price: float,
        category: Category,
        lessons: list
    ):
        self.title = name
        self.price = price
        self.category = category
        self.category.courses.append(self)
        self.lessons = lessons or []
    @staticmethod
    def create_course(title: str):
        courses = {}
        return courses.get(title)


class InteractiveCourse(Course):
    pass


class RecordedCourse(Course):
    pass


class CourseFactory:
    types = {"interactive": InteractiveCourse, "record": RecordedCourse}

    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)
