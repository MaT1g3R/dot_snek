from core import shell_command


def update():
    shell_command('git pull --recurse-submodules')
