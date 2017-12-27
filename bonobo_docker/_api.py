import os

from bonobo.util.api import ApiHelper

__all__ = []

api = ApiHelper(__all__=__all__)


@api.register_graph
def runc(
    graph,
    *,
    plugins=None,
    services=None,
    strategy=None,
    environ=None,
    shell=False,
    volumes=None,
    with_local_packages=False
):
    from bonobo_docker.utils import run_docker, get_volumes_args, get_image

    site_volumes = get_volumes_args(with_local_packages=with_local_packages)

    if shell:
        command = '/bin/bash'
    elif graph.file:
        target = os.path.realpath(os.path.join(os.getcwd(), graph.file))

        if os.path.isdir(target):
            site_volumes += ('-v ' + target + ':/home/bonobo/app', )
            command = "bin/bonobo run --install app"
        elif os.path.isfile(target):
            site_volumes += ('-v ' + os.path.dirname(target) + ':/home/bonobo/app', )
            command = "bin/bonobo run --install app/" + os.path.basename(target)
        else:
            raise IOError(
                'File does not exist, or is of unsupported type (only directories and regular files are supported).'
            )
    elif graph.mod:
        raise NotImplementedError('Executing a module within a docker container is not yet implemented.')
    else:
        command = '/home/bonobo/bin/python'

    run_docker(
        'run -it --rm',
        *site_volumes,
        *(['-v {}'.format(v) for v in volumes] if volumes else []),
        get_image(),
        command,
    )
