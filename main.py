from os.path import expanduser
from pathlib import Path
from sys import argv

from snek.core import link_all
from snek.update import update

if __name__ == '__main__':
    if argv[1].lower() == 'update':
        update()
    if argv[1] == 'link':
        environments = argv[2:]
        for e in environments:
            link_all(Path(f'../{e}').resolve(), Path(expanduser('~')))
