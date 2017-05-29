from os import chdir, getcwd
from pathlib import Path

from snek.core import shell_command


def update():
    """
    Pull all changes from the git repo to local
    """
    old_dir = getcwd()
    chdir(Path('..').absolute())
    shell_command('git submodule update --init --recursive')
    shell_command('git pull')
    chdir(old_dir)



