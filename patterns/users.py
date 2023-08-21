class User:
    def __init__(self):
        self.email = None
        self.password = None


class Teacher(User):
    pass


class Student(User):
    pass


class Staff(User):
    def __init__(self):
        self.permission = None
        super().__init__()


class UserFactory:
    types = {"student": Student, "teacher": Teacher, "staff": Staff}

    @classmethod
    def create(cls, type_: str):
        return cls.types[type_]()
