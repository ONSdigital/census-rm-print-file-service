class TemplateNotFoundError(Exception):
    pass


class MalformedMessageError(Exception):
    pass


class EncryptionFailedException(Exception):
    pass


class DaemonStartupError(Exception):
    pass
