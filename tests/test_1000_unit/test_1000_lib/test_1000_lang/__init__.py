def test_lazy_object():
    from watdafduge.lib.lang import LazyObject

    obj = LazyObject()

    import logging
    assert isinstance(obj.logger, logging.Logger)

    if obj.ipython is None:
        try:
            ipy = get_ipython()
        except NameError:
            ipy = None
        
        assert ipy is None
    else:
        assert obj.ipython is get_ipython()
        