from src.domain.exceptions.api_exception import ApiException


class UserAlreadyExistsError(ApiException):
    pass

class UserNotFountError(ApiException):
    pass