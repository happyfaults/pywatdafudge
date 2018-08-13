# PyWatDaFudge (PyWTF)
A Python library to detect profanity and measure toxicity of text documents (ie. online comments)

#
## Quickstart Install
Currently, the library has only been tested with [Python 3.6.6](https://www.python.org/downloads/release/python-366/).

To install everything using [pip](https://pypi.org/project/pip/), issue the following commands from the project root directory:

1. pip install -r requirements.txt
2. pip install -e .
3. pip install -e config/

Leave out the -e if you want to install the packages into your Python site folder.

You can also use the equivalent python setup commands:

1. pip install -r requirements.txt
2. python setup.py develop (or install)
3. python config/setup.py develop (or install)

#
## Requirements

Currently, the library supports two methods for detecting profanity as follows.
### Regex

This method uses regular expressions to match documents against a list of phrases cached in memory.

There are no extra dependencies required for this method.

### Whoosh

This method creates a [Whoosh](http://whoosh.readthedocs.io/en/latest/intro.html) search index of the list of phrases. Documents are then split into various word-ngrams to produced phrases to search against the Whoosh index.

#### Dependencies:
1. [numpy](http://www.numpy.org/)
2. [nltk](https://www.nltk.org/)
3. whoosh

To install the dependencies:

`pip install -r requriements.txt`

#
### Example Usage
```python
def wp_use_case(docs_dir, phrases_dir, results_dir, demunge=False):
    """Setting demunge=True will enable demunging of text documents.

    For example:
    1. The character '@' will get replace with 'a'.

    See module watdafudge.nltools.demunger for more details.
    """
    from os import path
    
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

    # load the files-based app interactor (context)
    from watdafudge.client.files import App
    a = App.Load()

    for method in ('regex', 'whoosh',):
        docs = a.analyze(
            docs_dir,
            phrases_files=phrases_files,
            demunge=demunge,
            method=method
        )

        dst_path = path.join(
            results_dir,
            f'actual_results-{method}.txt'
        )

        results = {}
        for d in a.serializeDocs(docs, dst_path):
            results[d['name']] = int(d['score'])

        return results

```
#
## Configuration
All configuration is done using a framework that sets items to a Python dict when the app is loaded.
```python
>>> from watdafudge.client.files import App
>>> a = App.Load()
>>> a.config
{'.NS': 'watdafudge',
 'watdafudge.prefix': 'files',
 'watdafudge.now_dt': datetime.datetime(2018, 8, 13, 14, 33, 30, 175158),
 'watdafudge.working_dir': '/home/hendrix/dev/pywatdafudge',
 'watdafudge.level_code': 10,
 'watdafudge.logging_dir': '/home/hendrix/dev/pywatdafudge/logs',
...
}
```
#### Namespaces
For convenience, you can access and update configuration items using a namespace type variable.
```python
>>> NS = a.config['.NS']
>>> NS
'watdafudge'
>>> RootNS = a.RootNS
>>> assert NS == RootNS
>>> assert NS == 'watdafudge'
>>> a.config[NS.logging_dir]
'/home/hendrix/dev/pywatdafudge/logs'
>>> NS.logging_dir
'watdafudge.logging_dir'
>>> a.config['watdafudge.logging_dir']
'/home/hendrix/dev/pywatdafudge/logs'
```
To access the settings for the regex and whoosh analyzers
```python
>>> a.config[NS.analyzers.regex]
{}
>>> whoosh_settings = a.config[NS.analyzers.whoosh]
>>> whoosh_settings
{'index_dir': 'wtf_index', 'word_ngrams_max': 3, 'slop_factor': 2}
>>> whoosh_settings['index_dir'] = 'new_wtf_index'
```
### Config Modules
From the project directory, you can find the default configuration modules in the subfolder: config/watdafudge_c

So the configuration module for the app: `watdafudge.client.files.App`

Is the corresponding match type: `watdafudge_c.client.files.App`

To change defauls, see file: `config/watdafudge_c/client/files/__init__.py`

If you do not install the watdafudge_c package, the root config path must be included in your PYTHONPATH environment variable so that configuration modules can be imported.
```python
>>> import watdafudge_c
>>>
```
    
## TDD & CI

This library is being developed using the agile principles of [test-driven development (TDD)](http://agiledata.org/essays/tdd.html) and [continous integration (CI)](https://www.atlassian.com/continuous-delivery/ci-vs-ci-vs-cd).

Testing is done with [Pytest](https://docs.pytest.org/en/latest/). 

This repository is connected to [Travis-CI](https://travis-ci.org/happyfaults/pywatdafudge).

## Development Roadmap

At this time, the library is being developed as a proof-of-concept.

It is being tested against [Python 3.6.6](https://www.python.org/downloads/release/python-366/) only at the moment.

There may be an effort to support [Python 2.7.15](https://www.python.org/downloads/release/python-2715/) and the [Python 3.5](https://www.python.org/downloads/release/python-356/) earlier versions.

However, the goal is to use the library as part of a [RESTful](https://www.restapitutorial.com/) [Microservice](https://en.wikipedia.org/wiki/Microservices) solution for the [Kaggle's Toxic Comment Classification Challenge](https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge).

So new features like [asyncio](https://docs.python.org/3/library/asyncio.html) that are only available for Python 3.6+ may be utilized.