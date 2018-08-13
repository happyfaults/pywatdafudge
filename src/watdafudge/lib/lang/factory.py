from . import LazyObject

class Factory(LazyObject):
    """A simple interface for a Factory type.

    Examples:
        >>> Factory.Default(cfg)
    """
    @classmethod
    def Default(cls, config):
        return cls(config)

    def __init__(self, config):
        self.config = config
    

class FactoryClient(LazyObject):

    DefaultFactory = Factory.Default

    @classmethod
    def Default(cls, config):
        return cls(config)

    def __init__(self, config):
        self.config = config

    def set_factory(self):
        self.factory = self.DefaultFactory(self.config)
        return self.factory