r"""
Errors Module
-------------

The module defined error class used throughout the pyweather
package to handle various exceptional scenarios.
"""


class RequestError(Exception):
    r"""
    RequestError class for handling API requests errors.

    This exception is raised when there's an error during API requests,
    encompassing various issues such as server-related errors
    (e.g., HTTP status codes other than 200).
    """

    def __init__(self, status_code: int, message: str | None = None) -> None:
        message = f"Server responded with status code {status_code}. {message}"
        super().__init__(message)
