from . import Analyzer as BaseAnalyzer, \
    Factory as BaseFactory

class Factory(BaseFactory):
    pass

class Analyzer(BaseAnalyzer):

    DefaultFactory = Factory

    @classmethod
    def Default(cls, match_phrases=None, config=**kwargs):
        if match_phrases is None:
            match_phrases = []
        return cls(match_phrases)

    def __init__(self, match_phrases):
        self.match_phrases = match_phrases
    
    def set_settings(self):
        config = self.config
        NS = config['.NS']
        self.settings = config[NS.analyzers.regex]
        return self.settings

    def addPhrases(self, phrases, weight=1.0):
        from re import compile, \
            escape, \
            I as RE_IGNORE_CASE

        match_phrases = self.match_phrases
        
        for p in phrases:
            # we use a regex pattern that is
            # case-insensitive with word-boundary
            p_list = [p['name']]
            if 'content' in p and p['content'] != p['name']:
                p_list.extend(
                    s.strip()
                    for s in p['content'].split(u',')
                )
                
            pat = u'|'.join(
                r'\b%s\b' % escape(s)
                for s in p_list
            )

            match_phrases.append({
                'name': p[u'name'],
                'match': compile(
                    r'.*(%s).*' % pat,
                    RE_IGNORE_CASE
                ).findall,
                'weight': p.get('weight', weight),
            })

        return self

    def score(self, docs, demunge=False):

        #settings = self.settings

        if demunge is True:
            demunge = self.text_demunger_factory().process
        elif not callable(demunge):
            demunge = lambda t: t
        
        match_phrases = self.match_phrases
        for d in docs:
            s = 0.0
            matches = []
            for i in match_phrases:
                text = demunge(d['text'])
                res = i['match'](text)
                if res:
                    s += i['weight'] #* len(res)
                    matches.extend(res)

            d['score'] = s
            d['matches'] = matches

            yield d

