from ..lib.lang.factory import Factory as BaseFactory, FactoryClient

class Factory(BaseFactory):

    def getTextDemungerFactory(self):
        from watdafudge.nltools.demunger import TextDemunger
        return TextDemunger.Default

class Analyzer(FactoryClient):
    
    DefaultFactory = Factory.Default

    def set_text_demunger_factory(self):
        self.text_demunger_factory = self.factory.getTextDemungerFactory()
        return self.text_demunger_factory
    
    def close(self):
        return self

    def addPhrases(self, phrases, weight=1.0):
        raise NotImplementedError

    def score(self, docs, demunage=False):
        raise NotImplementedError

