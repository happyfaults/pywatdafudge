from ..lib.lang import LazyObject

class DocsLoader(LazyObject):

    def __iter__(self):
        raise NotImplementedError


