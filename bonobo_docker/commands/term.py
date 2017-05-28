import os

import bonobo
from bonobo_docker import settings
from bonobo_docker.utils import run_docker


def get_volumes(pristine=False):
    cache_path = os.path.expanduser('~/.cache')
    volumes = {}
    volumes[cache_path] = {'bind': '/home/bonobo/.cache'}
    if not pristine:
        from bonobo.util.pkgs import bonobo_packages
        for name in bonobo_packages:
            volumes[bonobo_packages[name].location] = {'bind': '/home/bonobo/src/' + name}
    return volumes


def get_volumes_args(pristine=False):
    for hostpath, volumespec in get_volumes(pristine=pristine).items():
        yield '-v {}:{}{}'.format(hostpath, volumespec['bind'], ':ro' if volumespec.get('mode') == 'ro' else '')


def execute(clear=False, pristine=False):
    """
    :param file file:
    :return:
    """

    if clear:
        os.system('clear')

    run_docker(
        'run -it --rm --user bonobo',
        *get_volumes_args(pristine=pristine),
        '{}:{}'.format(settings.IMAGE, bonobo.__version__),
        'bash',
    )


def register(parser):
    parser.add_argument('--clear', action='store_true')
    parser.add_argument('--pristine', action='store_true')
    return execute
