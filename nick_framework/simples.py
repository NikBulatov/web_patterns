from enum import Enum


class Format(Enum):
    ONLINE = "online"
    OFFLINE = "offline"


class Technique(Enum):
    SIMPLE = "simple"
    SIMULTANEOUS = "simultaneous"
    TRADITIONAL = "traditional"
    COMPLEX = "complex"