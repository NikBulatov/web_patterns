from copy import deepcopy

from patterns.users import Student


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
