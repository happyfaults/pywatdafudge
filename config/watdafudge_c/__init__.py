from builtins import object

class Config(object):

    @classmethod
    def Load(cls, context_cls, cfg):
        return cls.LoadBase(
            context_cls,
            cfg
        ).LoadLogging(
            context_cls,
            cfg
        ).LoadExtend(
            context_cls,
            cfg
        )

    @classmethod
    def LoadExtend(cls, context_cls, cfg):
        """Classes shoud override this method with 
        to add addition cfgiguration values as needed.
        """
        return cls

    @classmethod
    def LoadBase(cls, context_cls, cfg):
        from os import path
        
        NS = cfg['.NS']
        
        now = cfg[NS.now_dt]
        cfg.update({
            NS.logging_dir : path.join(cfg[NS.working_dir], 'logs'),
            NS.default_encoding : {
                'codec' : 'utf-8',
                'errors' : 'strict' #ignore
            },
            NS.now_str : '%d_%02d_%02d_%02d_%02d_%02d' % (
                now.year, now.month, now.day,
                now.hour, now.minute, now.second
            )
        })
        
        return cls

    @classmethod
    def LoadLogging(cls, context_cls, cfg):
        from os import path
        
        NS = cfg['.NS']
               
        prefix = '%s-%s' % (
            cfg[NS.prefix],
            cfg[NS.now_str]
        )
        
        log_dir = cfg[NS.logging_dir]
        
        cfg[NS.logging_prefix] = prefix
        cfg[NS.logging] = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'simple': {
                    'format': '%(asctime)s|%(name)s|%(levelname)s: %(message)s'
                }
            },
        
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'level': 'CRITICAL',
                    'formatter': 'simple',
                    'stream': 'ext://sys.stdout'
                },
        
                'info_file_handler': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'level': 'INFO',
                    'formatter': 'simple',
                    'filename': path.join(log_dir, '%s-info.log' % prefix),
                    'maxBytes': 10485760,
                    'backupCount': 20,
                    'encoding': 'utf8'
                },
        
                'error_file_handler': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'level': 'ERROR',
                    'formatter': 'simple',
                    'filename': path.join(log_dir, '%s-errors.log' % prefix),
                    'maxBytes': 10485760,
                    'backupCount': 20,
                    'encoding': 'utf8'
                }
            },
        
            'loggers': {
                context_cls.ROOT_NS: {
                    'level': 'INFO',
                    'handlers': [
                        'console', 'info_file_handler', 'error_file_handler'
                    ],
                    'propagate': 'no'
                },
                'py.warnings': {
                    'level': 'WARN',
                    'handlers': [
                        'console', 'info_file_handler', 'error_file_handler'
                    ],
                    'propagate': 'no'
                }
            },
        
            #'root': {
            #    'level': 'CRITICAL',
            #    'handlers': [
            #        'console',
            #    ]
            #}
        }
        
        cfg[NS.logging_capture_warnings] = True
        
        return cls
    
