import os

import bonobo
from bonobo.util.pkgs import bonobo_packages
from bonobo_docker import settings
from bonobo_docker.utils import run_docker


def get_volumes():
    cache_path = os.path.expanduser('~/.cache')
    volumes = {}
    volumes[cache_path] = {'bind': '/home/bonobo/.cache'}
    for name in bonobo_packages:
        volumes[bonobo_packages[name].location] = {'bind': '/home/bonobo/src/' + name}
    return volumes


def get_volumes_args():
    for hostpath, volumespec in get_volumes().items():
        yield '-v {}:{}{}'.format(hostpath, volumespec['bind'], ':ro' if volumespec.get('mode') == 'ro' else '')


def execute(clear=False):
    """
    :param file file:
    :return:
    """

    if clear:
        os.system('clear')

    run_docker(
        'run -it --rm --user bonobo',
        *get_volumes_args(),
        '{}:{}'.format(settings.IMAGE, bonobo.__version__),
        'bash',
    )


def register(parser):
    parser.add_argument('--clear', action='store_true')
    return execute
