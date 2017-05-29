from pathlib import Path
from sys import argv

from snek.core import link_all
from snek.update import update

if __name__ == '__main__':
    if argv[0].lower() == 'update':
        update()
    if argv[0] == 'link':
        environments = argv[1]
        for e in environments:
            link_all(Path(f'../@{e}'), Path('~/'))
