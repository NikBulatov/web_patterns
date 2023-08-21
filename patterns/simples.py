from enum import Enum


class Technique(Enum):
    SIMULTANEOUS = "simultaneous"
    TRADITIONAL = "traditional"
    COMPLEX = "complex"


class Level(Enum):
    JUNIOR = "junior"
    MIDDLE = "middle"
    SENIOR = "senior"