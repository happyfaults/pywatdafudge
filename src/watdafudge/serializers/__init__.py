from ..lib.lang.factory import Factory, FactoryClient

class Factory(Factory):
    pass

class Serializer(FactoryClient):

    DefaultFactory = Factory.Default
    
    def serializeDocs(self, fout, docs):
        raise NotImplementedError