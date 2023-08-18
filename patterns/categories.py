class Category:
    increment = 0

    def __init__(self, name: str, category):
        self.id = Category.increment
        Category.increment += 1
        self.name = name
        self.category = category
        self.courses: list = []

    def course_count(self):
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
        return result
