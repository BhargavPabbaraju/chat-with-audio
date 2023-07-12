from enum import Enum


class FileType(Enum):
    FILE = 0
    RECORD = 1
    YOUTUBE = 2


class Language(str, Enum):
    US_ENGLISH = "en-US"
    IN_ENGLISH = "en-IN"
    TELUGU = "te-IN"
    HINDI = "hi-IN"
    JAPANESE = "ja-JA"
