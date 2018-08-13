
from ..lang import LazyObject

#from contextlib import contextmanager

class Manager(LazyObject):
    """A manager type for encapsulating connections to persistent storage types.

    Examples:
        >>> conn_mgr = Manager.Default(cfg)
        >>> adapter = conn_mgr.connectCassandra(...)

    """

    @classmethod
    def Default(cls, config):
        return cls(config)
    
    def __init__(self, config):
        self.config = config
        
    # add connect ,ethods latter as needed.
    