from builtins import object

class LazyObject(object):
    """A lazy object type where attributes are set for the first-time 
    when matching method set_{attribute}.

    Examples:

        class MyLazyObject(LazyObject):
            # no attribute for is_available
            def set_is_available(self):
                self.is_available = True
                return self.is_available

        >>> o = MyLazyObject()
        >>> a.is_available
        True

    """
    
    def __getattr__ (self, key):
        if key.startswith('set_'):
            raise AttributeError(key[4:])
        return getattr(self, 'set_%s' % key)()
   
    def set_logger(self):
        import logging
        self.logger = logging.getLogger(
            self.__class__.__module__ #, self.__class__.__name__
        )
        return self.logger
    
    def set_ipython(self):
        try:
            self.ipython = get_ipython()
        except NameError:
            self.ipython = None
        return self.ipython

    def set_pdb(self):
        if self.ipython:
            import ipdb
            self.pdb = ipdb
        else:
            import pdb
            self.pdb = pdb
        return self.pdb
        