import os

import bonobo
from bonobo.commands.run import register_generic_run_arguments
from bonobo_docker.commands.shell import get_volumes
from bonobo_docker.services import client


def register(parser):
    register_generic_run_arguments(parser)
    return execute


def execute(filename, module, quiet=False, verbose=False):
    from bonobo_docker import settings

    target = os.path.realpath(os.path.join(os.getcwd(), filename))

    volumes = get_volumes()

    if filename:
        if os.path.isdir(target):
            volumes[target] = {'bind': '/home/bonobo/app', 'mode': 'ro'}
            command = "bin/bonobo run --install app"
        elif os.path.isfile(target):
            volumes[os.path.dirname(target)] = {'bind': '/home/bonobo/app', 'mode': 'ro'}
            command = "bin/bonobo run app/" + os.path.basename(target)
        else:
            raise IOError(
                'File does not exist, or is of unsupported type (only directories and regular files are supported).'
            )
    elif module:
        raise NotImplementedError('Not yet implemented.')
    else:
        raise RuntimeError('UNEXPECTED: argparse should not allow this.')

    container = client.containers.run(
        '{}:{}'.format(settings.IMAGE, bonobo.__version__),
        command=command,
        user='bonobo',
        detach=True,
        volumes=volumes
    )
    for line in container.logs(stream=True):
        print(line.decode('utf-8'), end='')
