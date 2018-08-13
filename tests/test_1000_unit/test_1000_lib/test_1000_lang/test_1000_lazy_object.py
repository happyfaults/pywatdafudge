from watdafudge import pytest

def test_1000_lazy_object():
    
    from watdafudge.lib.lang import LazyObject

    obj = LazyObject()

    import logging
    assert isinstance(obj.logger, logging.Logger)

    if obj.ipython is None:
        try:
            ipy = get_ipython()
        except NameError:
            ipy = None
        
        assert ipy is None

        import pdb
        assert obj.pdb is pdb

    else:
        assert obj.ipython is get_ipython()

        import ipdb
        assert obj.pdb is ipdb

    with pytest.raises(AttributeError):
        attr = obj.this_attr_does_not_exist
    
def test_1010_lazy_object_inherit():
    
    from watdafudge.lib.lang import LazyObject

    class MyObj(LazyObject):

        def __init__(self, val):
            self.val = val

        def set_myattr(self):
            self.myattr = self.val
            return self.myattr

        def set_val(self):
            self.val = -1
            return self.val

    obj = MyObj(1)
    assert obj.val == 1
    assert obj.myattr == 1

    del obj.val
    assert obj.val == -1
