from .. import Interactor

class App(Interactor):
    
    @classmethod
    def LoadExtend(cls, context_type, cfg):

        _NS = cfg['.NS']

        NS = _NS.analyzers

        cfg.update({
            NS.whoosh : {
                'index_dir': 'wtf_index',
                'word_ngrams_max': 3, 
                'slop_factor': 2
            },

            NS.regex : {

            }
        })

        NS = _NS.serializers.files
        cfg.update({
            NS.docs_simple_text : {
                'use_float_score': False,
            }
        })

        return cfg