_nop_init = lambda self, *args, **kw: None


class Singleton(object):
    """
    An abstractish class that can be used by inheritance to define Singletons - https://stackoverflow.com/a/59328423/4890123
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
            cls._instance._initialized = False
        elif cls.__init__ is not _nop_init:
            cls.__init__ = _nop_init
        return cls._instance
