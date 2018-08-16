
import pytest
import watdafudge
import watdafudge_c

watdafudge.pytest = pytest

def test_000_setup():
    
    from os import path

    tmp_dir = path.join(
        path.dirname(
            path.abspath(__file__)
        ),
        'tmp'
    )

    if path.exists(tmp_dir):
        try:
            import shutil
        except ModuleNotFoundError:
            import os
            if os.name == 'nt': # windows
                os.system(
                    f'rmdir {tmp_dir} /s'
                )
            else:
                os.system(
                    f'rm -rf {tmp_dir}'
                )
        else:
            shutil.rmtree(tmp_dir)

    from os import makedirs
    makedirs(tmp_dir)

    assert path.exists(tmp_dir)
    assert path.isdir(tmp_dir)

    watdafudge.TEST_TMP_DIR = tmp_dir
    watdafudge.test_mktmpdir = mktmpdir


def mktmpdir(basename, tmp_dir=None):
    
    if not tmp_dir:
        tmp_dir = watdafudge.TEST_TMP_DIR
    
    from os import path
    d = path.join(tmp_dir, basename)
    if not path.exists(d):
        from os import makedirs
        makedirs(d)
    
    assert path.isdir(d)
    
    return d

