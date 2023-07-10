from enum import Enum

class FileType(Enum):
    FILE = 0
    RECORD = 1

class Language(str,Enum):
    USENGLISH = 'en-US'