import http
from http.client import BAD_REQUEST


class IntegrityException(Exception):
    pass


class RelatedIntegrityError(Exception):
    pass


class HTTPError(Exception):
    def __init__(
        self,
        status_code: int = None,
        error_message: str = None,
        error_code: str = None,
    ) -> None:
        if status_code is None:
            status_code = BAD_REQUEST
        if error_message is None:
            error_message = http.HTTPStatus(status_code).phrase
        if error_code is None:
            error_code = http.HTTPStatus(  # pylint: disable=E1101
                status_code,
            ).name.lower()
        self.status_code = status_code
        self.error_code = error_code
        self.error_message = error_message

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return (
            f"{class_name}(status_code={self.status_code!r},"
            f"error_code={self.error_code!r},"
            f"error_message={self.error_message!r})"
        )