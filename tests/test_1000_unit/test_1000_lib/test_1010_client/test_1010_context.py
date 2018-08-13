from watdafudge import pytest

def test_1000_factory():
    from watdafudge.lib.client import Factory
    cfg = {
        'a': 1
    }
    f = Factory.Default(cfg)

    assert f.config is cfg
    
    from watdafudge.lib.client.conn import Manager as ConnMgr
    from watdafudge.lib.client.config import Manager as ConfigMgr

    assert isinstance(f.createConnMgr(), ConnMgr)
    assert isinstance(f.createConfigMgr(), ConfigMgr)


def test_1010_level():
    from watdafudge.lib.client import Level

    l = Level(Level.TEST)
    assert l.code == Level.TEST
    assert l.name == 'test'
    assert not l.isProduction()
    assert not l.isDevelopment()
    assert not l.isDebug()
    assert l.isTest()

    l.code = Level.PRODUCTION
    assert l.name == 'production'
    assert l.isProduction()
    assert not l.isDevelopment()
    assert not l.isDebug()
    assert not l.isTest()

    l.code = Level.DEVELOPMENT
    assert l.name == 'development'
    assert not l.isProduction()
    assert l.isDevelopment()
    assert not l.isDebug()
    assert not l.isTest()
    
    l.code = Level.DEBUG
    assert l.name == 'debug'
    assert not l.isProduction()
    assert not l.isDevelopment()
    assert l.isDebug()
    assert not l.isTest()

    l.code = -1
    assert l.name == 'unknown'
    assert not l.isTest()
    
def test_1020_context():

    from watdafudge.client import Interactor, Factory

    a = Interactor.Load()

    assert a.RootNS
    assert a.NS == a.RootNS[a.SUB_NS]

    assert a.level.isProduction()
    assert a.working_dir
    assert a.user_home_dir
    assert a.now_dt
