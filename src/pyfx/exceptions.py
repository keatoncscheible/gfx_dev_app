class KnobAlreadyExistsException(Exception):
    def __init__(self):
        super().__init__()


class KnobDoesNotExistException(Exception):
    def __init__(self):
        super().__init__()


class FootswitchAlreadyExistsException(Exception):
    def __init__(self):
        super().__init__()


class FootswitchDoesNotExistException(Exception):
    def __init__(self):
        super().__init__()


class PedalAlreadyExistsException(Exception):
    def __init__(self):
        super().__init__()


class PedalDoesNotExistException(Exception):
    def __init__(self):
        super().__init__()


class InvalidPedalConfigException(Exception):
    def __init__(self):
        super().__init__()


class UnsavedPedalChangesException(Exception):
    def __init__(self):
        super().__init__()


class PedalOverwriteException(Exception):
    def __init__(self):
        super().__init__()


class PedalConfigNotFoundException(Exception):
    def __init__(self):
        super().__init__()


class NewPedalConfigException(Exception):
    def __init__(self, message: str = None):
        super().__init__(message)


class PedalVariantAlreadyExistsException(Exception):
    def __init__(self):
        super().__init__()


class PedalVariantDoesNotExistException(Exception):
    def __init__(self):
        super().__init__()
