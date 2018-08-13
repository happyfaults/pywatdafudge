from . import Analyzer as BaseAnalyzer, Factory as BaseFactory

class Factory(BaseFactory):

    def openIndex(self):

        config = self.config
        NS = config['.NS']

        settings = config[NS.analyzers.whoosh]

        from whoosh.index import create_in, exists_in, open_dir
        
        from os import path, curdir
        index_dir = path.join(
            path.abspath(curdir),
            path.abspath(settings['index_dir'])
        )

        if not path.exists(index_dir):
            from os import makedirs
            makedirs(index_dir)
            return create_in(
                index_dir, 
                schema = self.schema            
            )

        elif not path.isdir(index_dir):
            raise ValueError(
                f'Path for index directory already exists as a non-directory resource: {index_dir}'
            )   

        # elif purge:
        #     from os import makedirs
        #     from shutil import rmtree
        #     rmtree(index_dir)
        #     makedirs(index_dir)
        #     return create_in(
        #         index_dir, 
        #         schema = self.schema
        #     )
        
        elif exists_in(index_dir):
            return open_dir(
                index_dir,
                schema = self.schema
            )

        return create_in(
            index_dir, 
            schema = self.schema
        )

    def set_schema(self):
        from whoosh.fields import Schema, \
            TEXT, NUMERIC, ID #, KEYWORD
        
        self.schema = Schema(
            name=ID(stored=True),
            weight=NUMERIC(stored=True),
            #keywords=KEYWORD(scorable=True),
            content=TEXT
        )
        return self.schema

    def createTextDemunger(self):
        from watdafudge.nltools.demunger import TextDemunger
        return TextDemunger.Default()

    def createWordTokenizer(self):
        from watdafudge.nltools.words import DefaultTokenizer
        return DefaultTokenizer()

    def getQParserFactory(self):
        from whoosh.qparser import \
            QueryParser, \
            FuzzyTermPlugin

        def factory(*args,**kwargs):
            p = QueryParser(*args, **kwargs)
            p.add_plugin(FuzzyTermPlugin)
            return p
            #p.remove_plugin_class(qparser.PhrasePlugin)
            #p.add_plugin(qparser.SequencePlugin())

        return factory


class Analyzer(BaseAnalyzer):

    DefaultFactory = Factory

    def set_settings(self):
        config = self.config
        NS = config['.NS']
        self.settings = config[NS.analyzers.whoosh]
        return self.settings

    def set_ix(self):
        self.ix = self.factory.openIndex()
        return self.ix
    
    def set_word_tokenizer(self):
        self.word_tokenizer = self.factory.createWordTokenizer()
        return self.word_tokenizer

    def set_text_demunger(self):
        self.text_demunger = self.factory.createTextDemunger()
        return self.text_demunger
    
    def set_qparser_factory(self):
        self.qparser_factory = self.factory.getQParserFactory()
        return self.qparser_factory

    def close(self):
        self.ix.close()
        return self

    def addPhrases(self, phrases, weight=1.0):

        ix_w = self.ix.writer()

        for p in phrases:
            ix_w.add_document(
                name = p['name'],
                content = p.get('content') or p['name'],
                weight = p.get('weight', weight)
            )

        ix_w.commit()

        return self

    def score(self, docs, demunge=False):

        settings = self.settings

        if demunge is True:
            demunge = self.text_demunger.process
        elif not callable(demunge):
            demunge = lambda t: t

        w_tokenize = self.word_tokenizer.tokenizer
        w_ngrams = self.word_tokenizer.ngrams
        
        slop = settings.get('slop_factor') or 1

        ix = self.ix
        with ix.searcher() as searcher:

            qparse = self.qparser_factory(
                'content', ix.schema
            ).parse

            search = searcher.search
            word_ngrams_max = settings['word_ngrams_max'] + 1

            for d in docs:
                words = w_tokenize(
                    demunge(d['text'])
                )
                matches = {}
                
               # _queries = [None,[],[],[]]

                for n in range(1, word_ngrams_max):
                    for r in w_ngrams(words, n):  
                        #r_ = demunge(r)
                        #if r != r_:
                        #    s = u'"{r}"~{slop} OR "{r_}"~{slop}'
                        #else:
                        #   s = u'"{r}"~{slop}'
                        s = u'"{r}"~{slop}'
                        q = qparse(
                            s.format(
                                r=r,
                                #r_=r_,
                                slop=slop
                            )
                        )

                        #_queries[n].append(q) # debug purposes
                        
                        results = search(q)
                        for hit in results:
                            m = matches.get(hit['name'])
                            if m:
                                if hit.score > m.score:
                                    matches[hit['name']] = hit
                            else:
                                matches[hit['name']] = hit
                            # we just need the top result
                            break 

                score = 0
                for hit in matches.values():
                    score += hit[u'weight'] #* hit.score

                d['score'] = score
                d['matches'] = matches
                
                # for debugging purposes
                #d['_queries'] = _queries

                yield d
