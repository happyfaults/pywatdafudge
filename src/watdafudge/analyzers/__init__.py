from ..lib.lang.factory import Factory as BaseFactory, FactoryClient

class Factory(BaseFactory):
    
    def createTextDemunger(self):
        from watdafudge.nltools.demunger import TextDemunger
        return TextDemunger.Default()


class Analyzer(FactoryClient):
    
    DefaultFactory = Factory.Default

    SETTINGS_KEY = None # override this key

    def set_settings(self):
        config = self.config
        NS = config['.NS']
        if self.SETTINGS_KEY:
            s = config.get(NS[self.SETTINGS_KEY])
            if s is None:
                s = {}
                self.settings = s
                config[NS[self.SETTINGS_KEY]] = s
            else:
                self.settings = s
        else:
            self.settings = {}

        return self.settings

    def set_text_demunger(self):
        self.text_demunger = self.factory.createTextDemunger()
        return self.text_demunger
    
    def close(self):
        return self

    def addPhrases(self, phrases, weight=1.0):
        raise NotImplementedError

    def score(self, docs, demunage=False):
        raise NotImplementedError

