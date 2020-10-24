from rambo import SingleActionEntryPoint, MultiActionEntryPoint
from .config import RedGiantConfig
from .project import RedGiantProject


class RedGiantSingleActionEntryPoint(SingleActionEntryPoint):

    def __init__(self):
        super().__init__()
        self.config = RedGiantConfig()

    def action(self) -> None:
        raise NotImplementedError


class RedGiantMultiActionEntryPoint(MultiActionEntryPoint):

    def __init__(self):
        super().__init__()
        self.config = RedGiantConfig()
