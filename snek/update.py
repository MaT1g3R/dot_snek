from os import chdir, getcwd
from pathlib import Path

from snek.core import shell_command


def update():
    """
    Pull all changes from the git repo to local
    """
    old_dir = getcwd()
    chdir(Path('..').absolute())
    shell_command('git submodule update --recursive --remote')
    shell_command('git add dot_snek')
    shell_command('git commit -m "snek"')
    shell_command('git push')
    shell_command('git pull')
    chdir(old_dir)
