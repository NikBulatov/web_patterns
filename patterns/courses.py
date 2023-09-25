from copy import deepcopy

from patterns.engine import Subject
from patterns.users import Student


class CoursePrototype:
    def clone(self):
        return deepcopy(self)


class Course(CoursePrototype, Subject):
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)
        self.students = []
        super().__init__()

    def __getitem__(self, item):
        return self.students[item]

    def add_student(self, student: Student):
        self.students.append(student)
        student.courses.append(self)
        self.notify()


class InteractiveCourse(Course):
    pass


class RecordCourse(Course):
    pass


class CourseFactory:
    types = {"interactive": InteractiveCourse, "record": RecordCourse}

    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)
