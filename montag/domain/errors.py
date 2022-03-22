class ApplicationError(Exception):
    """Base class for all application errors."""


class NotFoundError(ApplicationError):
    """Raised when an entity does not exists."""
