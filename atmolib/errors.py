"""
Errors Module
-------------

The module defines error classes for handling
various exceptional scenarios within the package.
"""


class RequestError(Exception):
    """
    RequestError class for handling API request errors.

    This exception is raised for all API endpoint requests returning
    a status code which do not fall in the 2xx series encompassing a
    failure in the request process.
    """

    def __init__(self, status_code: int, message: str | None = None) -> None:
        """
        Initializes the RequestError with a status
        code and an optional descriptive message.
        """

        message = f"Server responded with status code {status_code}. {message}"
        super().__init__(message)
