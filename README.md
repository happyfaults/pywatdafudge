# pywatdafudge
A Python library to detect profanity and measure toxicity of text documents (ie. online comments)

## Requirements

Currently, the library supports two methods for detecting profanity as follows.
### Regex

This method simply uses regular expressions to match documents against a list of phrases cached in memory.

There are no extra dependencies required for this method.

### Whoosh

This method creates a [Whoosh](http://whoosh.readthedocs.io/en/latest/intro.html) search index of the list of phrases. Documents are then split into various word-ngrams to produced phrases to search against the Whoosh index.

#### Dependences:
1. [numpy](http://www.numpy.org/)
2. [nltk](https://www.nltk.org/)
3. whoosh


### Example Usage

```python
def test_wp_use_case():

    from os import path

    files_dir = path.join(
        path.dirname(path.abspath(__file__)),
        'files',
        'case_wp_00'
    )

    docs_dir = path.join(
        files_dir,
        'inputs'
    )
    
    phrases_dir = path.join(
        files_dir,
        'phrases'
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

    from watdafudge.client.files import App
    a = App.Load()

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

```
## TDD & CI

This library is being developed using the agile principles of [test-driven development (TDD)](http://agiledata.org/essays/tdd.html) and [continous integration (CI)](https://www.atlassian.com/continuous-delivery/ci-vs-ci-vs-cd).

Testing is done with [Pytest](https://docs.pytest.org/en/latest/). 

This repository is connected to [Travis-CI](https://travis-ci.org/happyfaults/pywatdafudge).

## Development Roadmap

At this time, the library is being developed as a proof-of-concept.

It is being tested against [Python 3.6.6](https://www.python.org/downloads/release/python-366/) only.

There may be an effort to support [Python 2.7.15](https://www.python.org/downloads/release/python-2715/) and [Python 3.5.6](https://www.python.org/downloads/release/python-356/) versions.

However, the goal is to use the library as part of a [RESTful](https://www.restapitutorial.com/) [Microservice](https://en.wikipedia.org/wiki/Microservices) solution for the [Kaggle's Toxic Comment Classification Challenge](https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge).

So new features like [asyncio](https://docs.python.org/3/library/asyncio.html) that are only available for Python 3.6+ may be utilized.