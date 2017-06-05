import os

import bonobo
from bonobo.util.iterators import tuplize
from bonobo_docker import settings
from bonobo_docker.logging import logger


def run_docker(*args):
    cmd = ' '.join(('docker', ) + args)
    logger.info(cmd)
    return os.system(cmd)


def get_image():
    return '{}:{}'.format(settings.IMAGE, bonobo.__version__)


def get_volumes(*, with_local_packages=False):
    cache_path = os.path.expanduser('~/.cache')
    volumes = {}
    volumes[cache_path] = {'bind': '/home/bonobo/.cache'}
    if with_local_packages:
        from bonobo.util.pkgs import bonobo_packages
        for name in bonobo_packages:
            volumes[bonobo_packages[name].location] = {'bind': '/home/bonobo/src/' + name}
    return volumes


@tuplize
def get_volumes_args(*, with_local_packages=False):
    for hostpath, volumespec in get_volumes(with_local_packages=with_local_packages).items():
        yield '-v {}:{}{}'.format(hostpath, volumespec['bind'], ':ro' if volumespec.get('mode') == 'ro' else '')
