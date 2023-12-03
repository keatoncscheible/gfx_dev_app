from typing import Optional


class KnobAlreadyExistsError(Exception):
    def __init__(self):
        super().__init__()


class KnobDoesNotExistError(Exception):
    def __init__(self):
        super().__init__()


class FootswitchAlreadyExistsError(Exception):
    def __init__(self):
        super().__init__()


class FootswitchDoesNotExistError(Exception):
    def __init__(self):
        super().__init__()


class PedalAlreadyExistsError(Exception):
    def __init__(self):
        super().__init__()


class PedalDoesNotExistError(Exception):
    def __init__(self):
        super().__init__()


class InvalidPedalConfigError(Exception):
    def __init__(self):
        super().__init__()


class UnsavedPedalChangesError(Exception):
    def __init__(self):
        super().__init__()


class PedalOverwriteError(Exception):
    def __init__(self):
        super().__init__()


class PedalConfigNotFoundError(Exception):
    def __init__(self):
        super().__init__()


class NewPedalConfigError(Exception):
    def __init__(self, message: Optional[str] = None):
        super().__init__(message)


class PedalVariantAlreadyExistsError(Exception):
    def __init__(self):
        super().__init__()


class PedalVariantDoesNotExistError(Exception):
    def __init__(self):
        super().__init__()


class InvalidRootPedalFolderError(Exception):
    def __init__(self, message: Optional[str] = None):
        super().__init__(message)
