from enum import Enum


class FileType(Enum):
    FILE = 0
    RECORD = 1
    YOUTUBE = 2


class Language(str, Enum):
    US_English = "en-US"
    IN_English = "en-IN"
    UK_English = "en-GB"
    Bengali = "bn-BD"
    Chinese_Mandarin = "zh (cmn-Hans-CN)"
    French = "fr-FR"
    German = "de-DE"
    Gujarati = "gu-IN"
    Hindi = "hi-IN"
    Japanese = "ja-JA"
    Korean = "ko-KR"
    Malayalam = "ml-IN"
    Marathi = "mr-IN"
    Polish = "pl-PL"
    Portuguese = "pt-BR"
    Russian = "ru-RU"
    Spanish_Spain = "es-ES"
    Spanish_US = "es-US"
    Tamil = "ta-IN"
    Telugu = "te-IN"
    Thai = "th-TH"
    Vietnamese = "vi-VN"
