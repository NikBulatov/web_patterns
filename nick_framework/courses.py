# Origami courses
from simples import Format, Technique




class Course:
    def __init__(
        self,
        title: str,
        price: float,
        _format: Format = Format.ONLINE,
        technique: Technique = Technique.SIMPLE,
    ):
        self.title = title
        self.price = price
        self.format = _format
        self.technique = technique

    @staticmethod
    def create_course(title: str):
        courses = {}
        return courses.get(title)
