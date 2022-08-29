class Error(Exception):
    """Base class for other exceptions"""
    pass


class POpenError(Error):
    """Error while opening POpen"""
    pass


class InvalidArgument(Error):
    pass


class UnsupportedOS(Error):
    pass


class NotInitialized(Error):
    pass


class ClientError(Error):
    pass


class ExpectationNotMet(Error):
    pass


class AmbiguousMatch(Error):
    pass
