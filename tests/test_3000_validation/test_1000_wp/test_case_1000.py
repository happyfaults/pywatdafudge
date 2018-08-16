import watdafudge
from watdafudge import pytest

@pytest.fixture
def app():
    from watdafudge.client.files import App
    return App.Load()
    
@pytest.fixture
def files_dir():
    from os import path

    return path.join(
        path.dirname(
            path.abspath(__file__)
        ),
        'files'
    )

@pytest.fixture
def tmp_dir():
    return watdafudge.test_mktmpdir(
        'watdafudge_client_files'
    )


def test_1000_use_case(
    app, files_dir, tmp_dir
):
    """First TDD test case
    """
    from os import path

    files_dir = path.join(
        files_dir,
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
    
    NS = app.RootNS.analyzers
    whoosh_settings = app.config[NS.whoosh]
    whoosh_settings['index_dir'] = path.join(
        tmp_dir,
        'wp_1000_usecase-whoosh_wtf_index'
    )
    for m in ('regex', 'whoosh',):
        docs = app.analyze(
            docs_dir,
            phrases_files=phrases_files,
            method=m
        )

        dst_path = path.join(
            tmp_dir,
            f'wp_1000_usecase-actual_results-{m}.txt'
        )
        results = {}
        for d in app.serializeDocs(docs, dst_path):
            results[d['name']] = int(d['score'])

        assert results == expected_r, m
        


    