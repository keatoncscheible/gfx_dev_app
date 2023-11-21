class GfxPedalAlreadyExistsException(Exception):
    def __init__(self):
        super().__init__()


class GfxPedalDoesNotExistException(Exception):
    def __init__(self):
        super().__init__()


class GfxInvalidPedalConfigException(Exception):
    def __init__(self):
        super().__init__()


class GfxUnsavedPedalChangesException(Exception):
    def __init__(self):
        super().__init__()


class GfxPedalOverwriteException(Exception):
    def __init__(self):
        super().__init__()


class GfxPedalVariantAlreadyExistsException(Exception):
    def __init__(self):
        super().__init__()
