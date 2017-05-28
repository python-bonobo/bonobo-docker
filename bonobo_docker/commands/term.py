import os

import bonobo
from bonobo_docker import settings
from bonobo_docker.utils import run_docker
from bonobo_docker.volumes import get_volumes_args


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
