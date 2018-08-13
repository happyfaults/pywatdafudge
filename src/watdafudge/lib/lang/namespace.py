
class Type(str):
    """An enhanced str type that allows for cascading namespacing.

    Examples:
        >>> MyNS = Type('MyNS')
        >>> MyNS.a.b.c
        'MyNs.a.b.c'
    """
    @classmethod
    def FromObject(cls, obj):
        return cls(f'{obj.__module__}.{obj.__class__.__qualname__}')
        
    def __getitem__(self, name):
        return self.__class__(u'%s.%s' % (self, name))
    
    def __getattr__(self, name):
        return self.__class__(u'%s.%s' % (self, name))
    
    @property
    def parent(self):
        parts = self.split(u'.')
        if len(parts) > 1:
            return self.__class__(u'.'.join(parts[:-1]))
        return self
    
    @property
    def root(self):
        return self.__class__(self.split(u'.')[0])
    
    def fromMod(self, mod):
        return self.__class__(mod.__name__)
    
    def fromType(self, klass):
        return self.__class__(klass.__module__.__name__)
    
    def fromObj(self, obj):
        return self.__class__(obj.__class__.__module__.__name__)
    
    def new(self, name):
        return self.__class__(name)
        
        