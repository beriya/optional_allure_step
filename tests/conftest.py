"""Main test configuration."""
from functools import wraps

from allure_commons._allure import StepContext


class Step(StepContext):
    """Allure step wrapper."""

    def __init__(self, title: str, params: dict):
        super().__init__(title, params)
        self.__fake = False

    @property
    def fake(self) -> bool:
        """Return fake value."""
        return self.__fake

    @fake.setter
    def fake(self, fake: bool) -> None:
        """Set fake value."""
        self.__fake = fake

    def __enter__(self):
        if not self.__fake:
            super().__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.__fake:
            super().__exit__(exc_type, exc_val, exc_tb)

    def __call__(self, func):
        if not self.__fake:
            return super().__call__(func)

        @wraps(func)
        def impl(*args, **kwargs):
            with Step(self.title, self.params):
                return func(*args, **kwargs)

        return impl


def step(title: str) -> Step:
    """Provide step context."""
    if callable(title):
        return Step(title.__name__, {})(title)

    return Step(title, {})
