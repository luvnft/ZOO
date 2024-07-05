from enum import Enum


class Intents(Enum):
    USER_SIGNUP = "USER_SIGNUP"
    AUTH_GOOGLE = "AUTH_GOOGLE"
    SAVE_FILE = "SAVE_FILE"
    SAVE_DATA = "SAVE_DATA"
    ANSWER_QUERY = "ANSWER_QUERY"