# Origami models
from nick_framework.price import Price
from simples import Technique


class Model:
    def __init__(
        self,
        price: Price,
        instruction: str,
        level,
        technique: Technique = Technique.SIMPLE,
    ):
        self.price = price
        self.instruction = instruction
        self.level = level
        self.technique = technique
