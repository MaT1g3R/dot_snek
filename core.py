from codecs import decode
from os import rename, listdir
from os.path import isfile, basename, normpath, isdir, join
from subprocess import Popen, PIPE, STDOUT


def _rename(base, path):
    new = path.replace(base, 'dot-{}'.format(base[1:]))
    rename(path, new)
    return new


def rename_all(d: str):
    base = basename(normpath(d))
    if base in ('.git', '.gitignore', '.gitkeep'):
        return
    if isfile(d) and base.startswith('.') and base != '.directory':
        _rename(base, d)
    elif isdir(d):
        new_d = _rename(base, d) if base.startswith('.') else d
        for sub in listdir(new_d):
            rename_all(join(new_d, sub))


def shell_command(cmd):
    p = Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=True)
    for line in p.stdout:
        print(decode(line))
