from codecs import decode
from pathlib import Path
from subprocess import Popen, PIPE, STDOUT, call


def rename_all(path: Path, condition: callable, rename_: callable):
    """
    Recursively rename all files/directories under the input path

    :param path: the input path

    :param condition: a callable that returns True or False. If it returns
    false, the file/directory will be skipped for rename. It must take the
    file/directory's base name as the argument

    :param rename_: a callable that renames the file/directory and returns its
    new name. It must take the file/directory's base name as the first argument
    and the absolute path as the second argument.
    """
    if path.is_file() and condition(path):
        rename_(path)
    elif path.is_dir():
        path = rename_(path) if condition(path) else path
        for sub in path.iterdir():
            rename_all(path.joinpath(sub), condition, rename_)


def __base_cond(path: Path):
    """
    Base condition for all rename operations.
    :param path: the base file/dir path
    :return: True if the base file/dir name passed the base condition check
    """
    return path.name not in (
        '.git', '.gitignore', '.gitkeep', '.directory', '.gitmodules',
        '.github', '.travis.yml'
    )


def __get_rename(new_name: callable):
    """
    Returns a callable that takes file/directory's base name as the
    first argument and the absolute path as the second argument and
    renames the file/directory and returns its new name.

    :param new_name: a callable that takes a base file/directory name and
    returns its new base name as a string. It must take a base file/directory
    name as its only argument.

    :rtype: callable
    """

    def __rename(path: Path):
        new = str(path.absolute()).replace(path.name, new_name(path.name))
        path.rename(new)
        path.resolve()
        return Path(new)

    return __rename


def rename_to_hidden(path: Path):
    """
    Replace all file/dir under the root path with
    name that starts with "dot-" with "."

    :param path: the root file path object
    """
    rename_all(
        path,
        lambda x: __base_cond(x) and x.name.startswith('dot-'),
        __get_rename(lambda x: '.{}'.format(x[4:]))
    )


def rename_to_visible(path: Path):
    """
    Replace all file/dir under the root path with
    name that starts with "." with "dot-"

    :param path: the root file path object
    """
    rename_all(
        path,
        lambda x: __base_cond(x) and x.name.startswith('.'),
        __get_rename(lambda x: 'dot-{}'.format(x[1:]))
    )


def shell_command(cmd: str):
    """
    Run a shell command and prints its output to stdout
    :param cmd: the shell command
    """
    process = Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=True)
    for line in process.stdout:
        print(decode(line))


def create_symlink(src: Path, dest: Path):
    """
    Create a symlink from the src file to the dest directory

    :param src: the src file path

    :param dest: the dest dir path.
    """
    if not dest.parent.is_dir():
        dest.parent.mkdir(parents=True, exist_ok=True)
    assert src.is_file()
    assert dest.parent.is_dir()
    assert not dest.is_dir()
    if dest.exists():
        dest.unlink()
    dest.symlink_to(src)
    dest.resolve()


def __link_all(src: Path, dest: Path):
    """
    Recursively symlink all files under a the root path to the dest path
    :param src: the source path
    :param dest: the dest path
    """
    if __base_cond(src):
        if src.is_file():
            print('Linking {} to {}'.format(src, dest))
            create_symlink(src, dest)
        elif src.is_dir():
            for sub in src.iterdir():
                __link_all(src.joinpath(sub), dest.joinpath(sub.name))


def link_all(src: Path, dest: Path):
    """
    Link all your dot files from source to dest
    :param src: the source path
    :param dest: the dest path
    """
    call('clear', shell=True)
    print('Renaming...')
    rename_to_hidden(src)
    __link_all(src, dest)
    call('clear', shell=True)
    print('Renaming...')
    rename_to_visible(src)
    print('Done!')
