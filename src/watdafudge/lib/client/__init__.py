'''
Created on 2014-02-17

@author: Kia <kia@pcmusic.com>
'''
from builtins import object
from ..lang.factory import LazyObject, Factory

class Factory(Factory):
    """Base factory type for Context types.

    Examples:
        >>> f = Factory.Default(cfg)
        >>> cfg_mgr = f.createConfigMgr()
    """
    def createConnMgr(self):
        from .conn import Manager
        return Manager.Default(self.config)
    
    def createConfigMgr(self):
        from .config import Manager
        return Manager.Default()


class Level(object):
    """A type that keeps track of runtime level.

    Examples:
        >>> l = Level(Leve.TEST)
        >>> l.isProction()
        False
        >>> l.isTest()
        True
    """
    PRODUCTION = 10
    DEVELOPMENT = 20
    DEBUG = 30
    TEST = 40
    
    def __init__(self, code):
        self.code = code
        
    @property
    def name(self):
        if self.code == self.PRODUCTION:
            return 'production'
        if self.code == self.DEVELOPMENT:
            return 'development'
        if self.code == self.DEBUG:
            return 'debug'
        if self.code == self.TEST:
            return 'test'
        
        return 'unknown'
        
    def isProduction(self):
        return self.code == self.PRODUCTION
    
    def isDevelopment(self):
        return self.code == self.DEVELOPMENT
    
    def isDebug(self):
        return self.code == self.DEBUG
    
    def isTest(self):
        return self.code == self.TEST
        

class Context(LazyObject):
    """Base context type for creating interactors and "app" types 
    to provide clean api interfaces into the library. 

    Examples:
        >>> a = MyApp.Load()
        >>> a.processDocument(...)
    """

    name = ''    
    
    FactoryType = Factory.Default
    LevelType = Level
    DEFAULT_LEVEL = Level.PRODUCTION
    
    LOGGING_INIT_ALREADY_BY_CLS = None
    
    ROOT_NS = 'watdafudge'
    CONF_MODULE = 'watdafudge_c'
    
    @classmethod
    def InitLogging(cls, conf, level_code):
        import logging
        
        NS = conf['.NS']
        
        if cls.LOGGING_INIT_ALREADY_BY_CLS:
            logger = logging.getLogger('%s.%s' % (
                cls.__module__, cls.__name__
            ))
            logger.warn(
                f'Logging has already been initialized by class: {cls.LOGGING_INIT_ALREADY_BY_CLS}'
            )
            return cls
        
        Level = cls.LevelType
        
        ns = NS.logging_dir
        if ns in conf:
            import os
            if not os.path.isdir(conf[ns]):
                try:
                    os.makedirs(conf[ns])
                except OSError as e:
                    pass
        
        ns = NS.logging_level
        if ns in conf:
            logging.basicConfig(level=conf[ns])
            if level_code <= Level.PRODUCTION:
                del conf[ns]
        
        ns = NS.logging
        if ns in conf:
            from logging import config
            config.dictConfig(conf[ns])
            #if level_code <= Level.PRODUCTION:
            #    del conf[ns]
        
        # capture RuntimeWarnings from warnings module
        if conf[NS.logging_capture_warnings]:
            logging.captureWarnings(True)
        
        cls.LOGGING_INIT_ALREADY_BY_CLS = cls
        
        return cls
    
    @classmethod
    def Load(cls, working_dir='.', level_code=None, conf_module=None, factory_type=None, init_logging=True, now_dt=None, name=None):            
        
        if level_code is None:
            level_code = cls.DEFAULT_LEVEL
            
        if now_dt is None:
            from datetime import datetime
            now_dt = datetime.utcnow()
            
        if not name:
            name = cls.name

        from os.path import abspath
        from ..lang.namespace import Type
        
        NS = Type(cls.ROOT_NS)
        cfg = {
            '.NS' : NS,
            NS.prefix : name,
            NS.now_dt : now_dt,
            NS.working_dir : abspath(working_dir),
            NS.level_code : level_code
        }
        
        from .config import Manager
        if not conf_module:
            conf_module = cls.CONF_MODULE

        config_mgr = Manager.Default(conf_module)
        
        config_mgr.loadConfig(cls, cfg)
        if init_logging:
            cls.InitLogging(cfg, level_code)
        
        if factory_type is None:
            factory = cls.FactoryType(cfg)
        else:
            factory = factory_type(cfg)
        
        return cls(cfg, factory, name).init()
    
    
    def __init__(self, config, factory, name):
        self.config = config
        self.factory = factory
        self.name = name
        
    def init(self):
        return self
    
    def reloadConfig(self, working_dir='.', level_code=None, conf_module=None, factory_type=None, init_logger=False, now_dt=None):
        cls = self.__class__
                
        if level_code is None:
            level_code = cls.DEFAULT_LEVEL
            
        if now_dt is None:
            from datetime import datetime
            now_dt = datetime.utcnow()
            
        from os.path import abspath
        from ..lang.namespace import Type

        NS = Type(cls.ROOT_NS)
            
        cfg = {
            '.NS' : NS(cls.ROOT_NS),
            NS.prefix : self.name,
            NS.now_dt : now_dt,
            NS.working_dir : abspath(working_dir),
            NS.level_code : level_code
        }
        
        from config import Manager
        if not conf_module:
            conf_module = self.CONF_MODULE
        config_mgr = Manager.Default(CONF_MODULE)
        
        config_mgr.loadConfig(cls, cfg)
        if init_logger:
            cls.InitLogging(cfg, level_code)
        
        if factory_type is None:
            factory = cls.FactoryType(cfg)
        else:
            factory = factory_type(cfg)
        
        self.factory = factory
        
        return self.init()
    
    def set_RootNS(self):
        self.RootNS = self.config['.NS']
        return self.RootNS
    
    def set_NS(self):
        if self.SUB_NS:
            self.NS = self.RootNS[self.SUB_NS]
        else:
            from ..lang.namespace import Type
            self.NS = Type.FromObject(self)
        return self.NS
    
    def set_level(self):
        self.level = self.LevelType(
            self.config[self.RootNS.level_code]
        )
        return self.level
    
    def set_working_dir(self):
        self.working_dir = self.config[self.RootNS.working_dir]
        return self.working_dir
    
    def set_user_home_dir(self):
        from os.path import expanduser
        self.user_home_dir = expanduser('~')
        return self.user_home_dir
    
    def set_now_dt(self):
        self.now_dt = self.config[self.RootNS.now_dt]
        return self.now_dt

    