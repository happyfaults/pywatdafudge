def analyze(
    analyzer,
    docs_dir, 
    phrases_dir=None,
    phrases_files=None,
    docs_fpat=r'.+\.txt', 
    phrases_fpat=r'.+\.txt', 
    encoding='utf-8',
    demunge=False,
    weight=1.0
):
    
    if phrases_files:
        from ..data.files import PhrasesFileLoader
        for p in phrases_files:
            if isinstance(p, tuple):
                src_dir, w = p
            else:
                src_dir = p
                w = weight

            phrases = PhrasesFileLoader.Default(
                src_dir, 
                weight=w,  
                encoding=encoding
            )
            analyzer.addPhrases(phrases)

    if phrases_dir:
        from ..data.files import PhrasesDirLoader
        phrases = PhrasesDirLoader.Default(
            phrases_dir, 
            weight=weight, 
            fname_pat=phrases_fpat, 
            encoding=encoding
        )
        analyzer.addPhrases(phrases)

    from ..data.files import DocsDirLoader
    
    docs = DocsDirLoader.Default(
        docs_dir, 
        fname_pat=docs_fpat, 
        encoding=encoding
    )
       
    return analyzer.score(docs, demunge=demunge)


def regex_analyze(
    docs_dir, 
    phrases_dir=None,
    phrases_files=None, 
    docs_fpat=r'.+\.txt', 
    phrases_fpat=r'.+\.txt', 
    encoding='utf-8',
    demunge=False
):
    from ..analyzers.regex import Analyzer
    
    return analyze(
        Analyzer.Default(),
        docs_dir,
        phrases_dir,
        phrases_files,
        docs_fpat,
        phrases_fpat,
        encoding,
        demunge
    )

def whoosh_analyze(
    docs_dir, 
    phrases_dir=None,
    phrases_files=None,
    docs_fpat=r'.+\.txt', 
    phrases_fpat=r'.+\.txt', 
    encoding='utf-8',
    demunge=False,
    index_dir='wtf_index',
    word_ngrams_max=3, 
    slop_factor=2
):
    from ..analyzers.whoosh import Analyzer

    return analyze(
        Analyzer.Default(
            index_dir,
            word_ngrams_max=word_ngrams_max,
            slop_factor=slop_factor
        ),
        docs_dir,
        phrases_dir,
        phrases_files,
        docs_fpat,
        phrases_fpat,
        encoding,
        demunge
    )


def serialize_doc_scores_txt(
    docs, 
    dst_path='score_results.txt', 
    line_tmpl=None, 
    use_int_score=False,
    encoding='utf-8'
):

    from io import open
    from watdafudge.serializers.files import DocsSimpleTextSerializer

    with open(dst_path, 'w', encoding=encoding) as f:
        s = DocsSimpleTextSerializer.Default(line_tmpl, use_int_score)
        for d in s.serialize(f, docs):
            yield d

