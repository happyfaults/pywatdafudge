
<<<<<<< HEAD
def setup_path():
    import sys
    from os import path

    # add project src dir to path
    # as second highest priority after .
    test_dir = path.dirname(__file__)

    src_dir = path.join(
        path.dirname(test_dir),
        'src'
    )

    conf_dir = path.join(
        path.dirname(test_dir),
        'config'
    )

    sys.path.insert(
        1,
        src_dir
    )

    sys.path.insert(
        2,
        conf_dir
    )

    import watdafudge
    import watdafudge_c

import pytest
import watdafudge
import watdafudge_c

watdafudge.pytest = pytest

def test_setup():
    import sys, logging
    logging.getLogger().error(
        f'Path: {sys.path}'
    )

