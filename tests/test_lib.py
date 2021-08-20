"""Test - Library
"""

import os
import pathlib
import sys


def dir_up(depth):
    """Easy level-up folder(s)."""
    return sys.path.append(os.path.join(pathlib.Path(__file__).parents[depth], "src"))


# Append to (sys.path)
dir_up(1)


import project_name

project_name.pk1.hello()
project_name.pk2.hello()


print(
    dir(project_name)
)