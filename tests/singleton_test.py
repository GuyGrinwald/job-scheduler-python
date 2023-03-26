import logging

import pytest

from utils.singleton import Singleton

logger = logging.getLogger(__name__)


def test_singelton():
    obj1 = Singleton()
    obj2 = Singleton()
    assert obj1 == obj2


def test_singleton_inheritance():
    class SingletonInheritor(Singleton):
        def __init__(self, val: int) -> None:
            if hasattr(self, "val"):
                return
            self.val = val
            super().__init__(val)

    obj1 = SingletonInheritor(1)
    obj2 = SingletonInheritor(1)
    assert obj1 == obj2

    obj1.val = 2
    assert obj2.val == 2

    obj3 = SingletonInheritor(3)
    assert obj1 == obj3
    assert obj3.val == 2
