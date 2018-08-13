from . import Serializer as Serializer

class DocsSimpleTextSerializer(Serializer):

    LINE_TEMPLATE_DEFAULT = '{name}:{score:.0f}\n'
    LINE_TEMPLATE_FLOAT_SCORE = '{name}:{score:.2f}\n'

    def set_settings(self):
        config = self.config
        
        NS = config['.NS'].serializers.files
        self.settings = config[NS.docs_simple_text]

        return self.settings

    def serialize(self, fout, docs):
        settings = self.settings

        line_tmpl = settings.get('line_tmpl') 
        if not line_tmpl:
            if settings.get('use_float_score'):
                line_tmpl = self.LINE_TEMPLATE_FLOAT_SCORE.format
            else:
                line_tmpl = self.LINE_TEMPLATE_DEFAULT.format


        for d in docs:
            skip = yield d
            if skip:
                continue
                
            fout.write(
                line_tmpl(
                    **d
                )
            )
