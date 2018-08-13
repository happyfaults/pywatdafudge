from ..lib.client import Context, Factory


class Factory(Factory):
    """Base factory for all client interactors and apps.
    """
    pass

class Interactor(Context):
    """An Interactor provides top level api interface into the library.

    Examples:
        >>> a = MyInteractor.Load()
        >>> a.handleEvent(...)
    """
    FactoryType = Factory
    name = 'client'

    SUB_NS = 'client'