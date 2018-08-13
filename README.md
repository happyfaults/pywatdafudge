# PyWatDaFudge (PyWTF)
A Python library to detect and score text documents for risky phrases (ie. profanity in online comments).

## Quickstart Install
Currently, the library has only been tested with [Python 3.6.6](https://www.python.org/downloads/release/python-366/).

To install everything using [pip](https://pypi.org/project/pip/), issue the following commands from the project root directory:

1. pip install -r requirements.txt
2. pip install -e .
3. pip install -e config/

Leave out the **-e** switch if you want to install the packages into your Python site folder.

You can also use the equivalent Python setup commands:

1. pip install -r requirements.txt
2. python setup.py develop (or install)
3. python config/setup.py develop (or install)

## Requirements

Currently, the library supports two methods for detecting risky phrases as follows.
### Regex

This method uses regular expressions to match documents against a list of risky phrases cached in memory.

There are no extra dependencies required for this method.

### Whoosh

This method creates a [Whoosh](http://whoosh.readthedocs.io/en/latest/intro.html) search index of the risky phrases. Documents are then split into a specified range of **word-ngrams** to produce phrases that are then searched against the Whoosh index of risky phrases for *fuzzy* matches.

#### Dependencies:
1. [numpy](http://www.numpy.org/)
2. [nltk](https://www.nltk.org/)
3. whoosh

To install the dependencies:

`pip install -r requirements.txt`

You may also need to install the nlkt *punkt* language package:

`python -m nltk.downloader punkt`

## Example Usage
```python
def wp_use_case(docs_dir, phrases_dir, results_dir, demunge=False):
    """Setting demunge=True will enable demunging of text documents.

    For example:
    1. The character '@' will be replaced with an 'a' character.

    See module watdafudge.nltools.demunger for more details.
    """
    from os import path
    
    # A risky phrases file is assigned a default weight value
    # that will be applied to all contained phrases.
    # The weight is factored into phrase match scoring.
    #
    # For example:
    # Phrases from the low_risk_phrases.txt file will have a lower weighting
    # than phrases from the high_risk_phrases.txt file.
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

    # load the files-based app interactor type
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
            # the score value is a float
            results[d['name']] = int(d['score'])

        yield results, method, dst_path
```
See tests/test_3000_validation/test_1000_wp/test_case_1000.py for more details.

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
To access the settings for the regex and whoosh analyzers associated with this app
```python
>>> a.config[NS.analyzers.regex]
{}
>>> whoosh_settings = a.config[NS.analyzers.whoosh]
>>> whoosh_settings
{'index_dir': 'wtf_index', 'word_ngrams_max': 3, 'slop_factor': 2}
>>> whoosh_settings['index_dir'] = 'new_wtf_index'
```
### Config Modules
From the project directory, you can find the default configuration modules in the subfolder: `config/watdafudge_c`

So the configuration module for the app type: `watdafudge.client.files.App`

Is the corresponding matching type: `watdafudge_c.client.files.App`

To update the default values, see file: `config/watdafudge_c/client/files/__init__.py`

#### Ensure Config Modules Can Be Imported
If you do not install the **watdafudge_c** package, the root config path must be included in your **PYTHONPATH** environment variable so that the configuration modules can be imported when App.Load is called.
```python
>>> import watdafudge_c
>>>
```

## Logging
When executing the library with an app interactor type, log messages will be outputted to files. The configuration settings for logging can be accessed as follows:
```python
>>> a.config[NS.logging_dir]
'/home/hendrix/dev/pywatdafudge/logs'
>>> a.logger
<Logger watdafudge.client.files (INFO)>
>>> a.config[NS.logging]
{'version': 1,
 'disable_existing_loggers': False,
 'formatters': {'simple': {'format': '%(asctime)s|%(name)s|%(levelname)s: %(message)s'}},
 'handlers': {'console': {'class': 'logging.StreamHandler',
   'level': 'CRITICAL',
   'formatter': 'simple',
   'stream': 'ext://sys.stdout'},
  'info_file_handler': {'class': 'logging.handlers.RotatingFileHandler',
   'level': 'INFO',
   'formatter': 'simple',
   'filename': '/home/hendrix/dev/pywatdafudge/logs/files-2018_08_13_14_33_30-info.log',
   'maxBytes': 10485760,
   'backupCount': 20,
   'encoding': 'utf8'},
...
}
```
By default, in the log folder there will be two files for critical and non-critical messages respectively.
## TDD & CI

This library is being developed using the agile principles of [test-driven development (TDD)](http://agiledata.org/essays/tdd.html) and [continous integration (CI)](https://www.atlassian.com/continuous-delivery/ci-vs-ci-vs-cd).

Testing is done with [Pytest](https://docs.pytest.org/en/latest/). 

This repository is connected to [Travis-CI](https://travis-ci.org/happyfaults/pywatdafudge).

## Development Roadmap

At this time, the library is being developed as a proof-of-concept.

It is being tested against [Python 3.6.6](https://www.python.org/downloads/release/python-366/) only at the moment.

There may be an effort to support [Python 2.7.15](https://www.python.org/downloads/release/python-2715/) and the [Python 3.5](https://www.python.org/downloads/release/python-356/) and earlier versions.

However, a main goal of this library is to develop a [RESTful](https://www.restapitutorial.com/) [Microservices](https://en.wikipedia.org/wiki/Microservices) solution for the [Kaggle's Toxic Comment Classification Challenge](https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge).

So new features like [asyncio](https://docs.python.org/3/library/asyncio.html) that are currently only available for **Python 3.6+** may be utilized.