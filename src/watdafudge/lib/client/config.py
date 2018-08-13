
from ..lang import LazyObject

class Manager(LazyObject):
    """Manager type for loading configuration settings from Python modules as a dict.
    
    Examples:
        >>> cfg_mgr = Manager.Default()
        >>> cfg = {...}
        >>> cfg_mgr.loadConfig(MyInteractorApp, cfg)
    """
    @classmethod
    def Default(cls, base_modname='watdafudge_c', conf_d=None):
        from os import environ, path, curdir
        import sys
        
        if conf_d and conf_d not in sys.path:
            sys.path.append(path.abspath(conf_d))

        conf_d = path.join(curdir, 'config')
        if conf_d not in sys.path:
            sys.path.append(
                path.join(curdir, 'config')
            )

        if 'PYTHON_CLIENT_CONFIG_DIR' in environ \
            and environ['PYTHON_CLIENT_CONFIG_DIR'] not in sys.path:
            sys.path.append(environ['PYTHON_CLIENT_CONFIG_DIR'])
        
        if 'PYTHON_ENV_DIR' in environ:
            conf_d = path.join(
                environ['PYTHON_ENV_DIR'],
                'config'
            )
            if conf_d not in sys.path:
                sys.path.append(conf_d)
        
        if 'HOME' in environ:
            conf_d = path.join(environ['HOME'], '.pyconfig')
            if conf_d not in sys.path:
                sys.path.append(
                    conf_d
                )
        
        return cls(base_modname)
    
    def __init__(self, base_modname):
        self.base_modname = base_modname
        
    def loadConfig(self, context_type, conf):
        from importlib import import_module        
        
        m_name = context_type.__module__
        if m_name is None:
            m_name = self.base_modname
        else:
            m_name = m_name.split('.')[1:]
            if m_name:
                m_name = '%s.%s' % (
                    self.base_modname,
                    '.'.join(m_name)
                )
            else:
                m_name = self.base_module
        
        m = import_module(m_name)
        
        self.logger.info(f'Loaded Config Module {m.__name__}')
        
        cls = getattr(m, context_type.__name__)
        cls.Load(context_type, conf)
        
        context_type.CONFIG_TYPE = cls

        return self
        
    