from watdafudge import pytest

def test_0000_init():
    import watdafudge
    assert watdafudge.__version__

def test_1000_use_case():
    """First TDD test case
    """
    from watdafudge.client.files import App
    a = App.Load()
    