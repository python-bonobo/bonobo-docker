import os

from bonobo.commands.run import register_generic_run_arguments


def register(parser):
    register_generic_run_arguments(parser, required=False)
    parser.add_argument('--with-local-packages', '-L', action='store_true')
    parser.add_argument('--volume', '-v', action='append', dest='volumes')
    parser.add_argument('--shell', action='store_true')
    return execute


def execute(filename, module, volumes=None, shell=False, with_local_packages=False):
    from bonobo_docker.utils import run_docker, get_volumes_args, get_image

    site_volumes = get_volumes_args(with_local_packages=with_local_packages)

    if shell:
        command = "bash"
    elif filename:
        target = os.path.realpath(os.path.join(os.getcwd(), filename))

        if os.path.isdir(target):
            site_volumes += (target + ':/home/bonobo/app', )
            command = "bin/bonobo run --install app"
        elif os.path.isfile(target):
            site_volumes += (os.path.dirname(target) + ':/home/bonobo/app', )
            command = "bin/bonobo run app/" + os.path.basename(target)
        else:
            raise IOError(
                'File does not exist, or is of unsupported type (only directories and regular files are supported).'
            )
    elif module:
        raise NotImplementedError('Executing a module within a docker container is not yet implemented.')
    elif shell:
        command = '/bin/bash'
    else:
        command = '/home/bonobo/bin/python'

    run_docker(
        'run -it --rm',
        *site_volumes,
        *(['-v {}'.format(v) for v in volumes] if volumes else []),
        get_image(),
        command,
    )
