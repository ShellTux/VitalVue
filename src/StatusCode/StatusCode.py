from enum import Enum

class StatusCode(Enum):
    SUCCESS = 200
    API_ERROR = 400
    INTERNAL_ERROR = 500

    @staticmethod
    def fromCode(code: int):
        for c in StatusCode:
            if code != c.value:
                continue

            return c
