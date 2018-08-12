
import sys
from os import path

# add project src dir to path
# as second highest priority after .
test_dir = path.dirname(__file__)

src_dir = path.join(
    path.dirname(test_dir),
    'src'
)

sys.path.insert(
    1,
    src_dir
)

import watdafudge
