import os

import bonobo
from bonobo.util.packages import bonobo_packages
from bonobo_docker import settings
from bonobo_docker.utils import run_docker


def execute(clear=False):
    """
    :param file file:
    :return:
    """

    if clear:
        os.system('clear')

    cache_path = os.path.expanduser('~/.cache')
    run_docker(
        'run -it --rm --user bonobo',
        '-v {}:/home/bonobo/.cache'.format(cache_path),
        *('-v {}:/home/bonobo/src/{}'.format(bonobo_packages[name].location, name) for name in bonobo_packages),
        '{}:{}'.format(settings.IMAGE, bonobo.__version__),
        'bash',
    )


def register(parser):
    parser.add('--clear', action='store_true')
    return execute
