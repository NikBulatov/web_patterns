# Origami models
from simples import Technique, Level


class Model:
    def __init__(
        self,
        name: str,
        level: Level = Level.JUNIOR,
        technique: Technique = Technique.TRADITIONAL
    ):
        self.name = name
        self.level = level
        self.technique = technique
