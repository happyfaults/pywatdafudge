from watdafudge import pytest

def test_0000_init():
    import watdafudge
    assert watdafudge.__version__

def test_1000_use_case():
    """First TDD test case
    """
    from os import path

    from watdafudge.client.files import App
    a = App.Load()

    files_dir = path.join(
        path.dirname(path.abspath(__file__)),
        'files',
        'case_wp_00'
    )

    phrases_dir = path.join(
        files_dir,
        'phrases'
    )

    docs_dir = path.join(
        files_dir,
        'inputs'
    )
    phrases_files = (
        (
            path.join(
                phrases_dir,
                'low_risk_phrases.txt'
            ),
            1.0 #weight
        ),
        (
            path.join(
                phrases_dir,
                'high_risk_phrases.txt'
            ),
            2.0 #weight
        ),
    )

    import yaml

    expected_r = None
    with open(path.join(files_dir, 'expected_results.yml')) as f:
        expected_r = yaml.load(f)
    
    for m in ('regex', 'whoosh',):
        docs = a.analyze(
            docs_dir,
            phrases_files=phrases_files,
            method=m
        )

        dst_path = path.join(
            files_dir,
            f'actual_results-{m}.txt'
        )
        results = {}
        for d in a.serializeDocs(docs, dst_path):
            results[d['name']] = int(d['score'])

        assert results == expected_r, m
        


    