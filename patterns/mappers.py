from sqlite3 import connect, Connection, Cursor
from users import Student, Category, User
from exceptions import *

connection = connect("db.sqlite")


class StudentMapper:
    def __init__(self, connection: Connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.table_name = "student"

    def all(self):
        statement = f"SELECT * FROM {self.table_name}"
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id_, name = item
            student = Student(name)
            student.id = id_
            result.append(student)
        return result

    def find_by_id(self, id):
        statement = f"SELECT id, name FROM {self.table_name} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Student(*result)
        else:
            raise RecordNotFoundException(f"record with id={id} not found")

    def insert(self, obj):
        statement = f"INSERT INTO {self.table_name} (name) VALUES (?)"
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as error:
            raise DBCommitException(error.args)

    def update(self, obj):
        statement = f"UPDATE {self.table_name} SET name=? WHERE id=?"

        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as error:
            raise DBUpdateException(error.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.table_name} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as error:
            raise DBDeleteException(error.args)


class CategoryMapper:
    def __init__(self, connection: Connection):
        self.connection = connection
        self.cursor: Cursor = connection.cursor()
        self.table_name = "category"

    def all(self):
        statement = f"SELECT * FROM {self.table_name}"
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id_, name, category_ = item
            category = Category(name, category_)
            category.id = id_
            result.append(category)
        return result

    def find_by_id(self, id_):
        statement = f"SELECT id, name FROM {self.table_name} WHERE id=?"
        self.cursor.execute(statement, (id_,))
        result = self.cursor.fetchone()
        if result:
            return Category(*result)
        else:
            raise RecordNotFoundException(f"record with id={id_} not found")

    def insert(self, obj):
        statement = f"INSERT INTO {self.table_name} (name) VALUES (?)"
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as error:
            raise DBCommitException(error.args)

    def update(self, obj):
        statement = f"UPDATE {self.table_name} SET name=? WHERE id=?"

        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as error:
            raise DBUpdateException(error.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.table_name} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as error:
            raise DBDeleteException(error.args)


class MapperRegistry:
    mappers = {"student": StudentMapper, "category": CategoryMapper}

    @staticmethod
    def get_mapper(obj: User):
        if isinstance(obj, Student):
            return StudentMapper(connection)
        elif isinstance(obj, Category):
            return CategoryMapper(connection)

    @staticmethod
    def get_current_mapper(name: str):
        return MapperRegistry.mappers[name](connection)
