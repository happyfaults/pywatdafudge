from .. import Interactor, Factory


class Factory(Factory):
    """
    """
    
    def getPhrasesFileLoaderFactory(self):
        from watdafudge.data.files import PhrasesFileLoader
        return PhrasesFileLoader.Default

    def getPhrasesDirLoaderFactory(self):
        from watdafudge.data.files import PhrasesDirLoader
        return PhrasesDirLoader.Default

    def getDocsDirLoaderFactory(self):
        from watdafudge.data.files import DocsDirLoader
        return DocsDirLoader.Default

    def getAnalyzerFactory(self, method='regex'):

        if method == 'whoosh':
            from watdafudge.analyzers.whoosh import Analyzer
            return Analyzer.Default

        elif method == 'regex':
            from watdafudge.analyzers.whoosh import Analyzer
            return Analyzer.Default
        
        raise ValueError(
            f'Unknown method: {method}'
        )

    def getDocSerializerFactory(self, method='simple'):

        if method=='simple':
            from watdafudge.serializers.files import DocsSimpleTextSerializer
            return DocsSimpleTextSerializer.Default

        raise ValueError(
            f'Unknown method: {method}'
        )


class App(Interactor):
    """
    """
    FactoryType = Factory.Default
    name = 'files'

    def analyze(
        self,
        docs_dir, 
        phrases_dir=None,
        phrases_files=None,
        docs_fpat=r'.+\.txt', 
        phrases_fpat=r'.+\.txt', 
        encoding='utf-8',
        demunge=False,
        weight=1.0,
        method='regex'
    ):
        Analyzer = self.factory.getAnalyzerFactory(method)

        an = Analyzer(self.config)
        if phrases_files:
            PhrasesFileLoader = self.factory.getPhrasesFileLoaderFactory()
            for p in phrases_files:
                if isinstance(p, tuple):
                    src_path, w = p
                else:
                    src_path = p
                    w = weight

                phrases = PhrasesFileLoader(
                    src_path, 
                    weight=w,  
                    encoding=encoding
                )
                an.addPhrases(phrases)

        if phrases_dir:
            PhrasesDirLoader = self.factory.getPhrasesDirLoaderFactory()
            phrases = PhrasesDirLoader(
                phrases_dir, 
                weight=weight, 
                fname_pat=phrases_fpat, 
                encoding=encoding
            )
            an.addPhrases(phrases)

        DocsDirLoader = self.factory.getDocsDirLoaderFactory()
        
        docs = DocsDirLoader(
            docs_dir, 
            fname_pat=docs_fpat, 
            encoding=encoding
        )
        
        return an.score(docs, demunge=demunge)


    def serializeDocs(self, docs, dst_path, method='simple', encoding='utf-8'):

        F = self.factory.getDocSerializerFactory(method)
        with open(dst_path, 'w', encoding=encoding) as f:
            for d in F(self.config).serialize(f, docs):
                yield d

    