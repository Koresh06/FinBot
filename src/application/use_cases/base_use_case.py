from src.domain.exceptions.error_handlers import ErrorHandlingUtils


class BaseUseCase:
    def safe_execute(self, func, *args, error_message="Ошибка в use case", **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as ex:
            raise ErrorHandlingUtils.application_error(error_message, ex)
