from enum import Enum


class FileType(Enum):
    FILE = 0
    RECORD = 1


class Language(str, Enum):
    US_ENGLISH = "en-US"
