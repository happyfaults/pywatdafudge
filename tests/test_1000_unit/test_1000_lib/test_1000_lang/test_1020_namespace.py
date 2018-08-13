from watdafudge import pytest

def test_1000_namespace():

    from watdafudge.lib.lang.namespace import Type

    NS = Type('MyNS')
    assert NS == 'MyNS'
    assert NS.a.b.c == 'MyNS.a.b.c'
    assert NS.a.b.c.parent == 'MyNS.a.b'

    n = NS.a.b.c
    assert n.parent.parent.parent == NS