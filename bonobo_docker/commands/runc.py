import os
from contextlib import contextmanager

import bonobo_docker
from bonobo.commands import BaseGraphCommand
from bonobo.util.environ import parse_args, get_argument_parser


class GraphReference:
    def __init__(self, file, mod):
        assert bool(file) != bool(mod), "You can only provide file or module, not both."
        self.file = file
        self.mod = mod

class RuncCommand(BaseGraphCommand):
    install = False
    handler = staticmethod(bonobo_docker.runc)

    def add_arguments(self, parser):
        super(RuncCommand, self).add_arguments(parser)

        parser.add_argument('--with-local-packages', '-L', action='store_true')
        parser.add_argument('--volume', '-v', action='append', dest='volumes')
        parser.add_argument('--shell', action='store_true')

    @contextmanager
    def read(self, file, mod, **options):
        _environ, os.environ = os.environ, {}
        try:
            with parse_args(options) as options:
                options['environ'] = os.environ
                yield GraphReference(file, mod), {}, options
        finally:
            os.environ = _environ

    def execute(self, filename, module, volumes=None, shell=False, with_local_packages=False):
        from bonobo_docker.utils import run_docker, get_volumes_args, get_image

        site_volumes = get_volumes_args(with_local_packages=with_local_packages)

        if shell:
            command = '/bin/bash'
        elif filename:
            target = os.path.realpath(os.path.join(os.getcwd(), filename))

            if os.path.isdir(target):
                site_volumes += ('-v ' + target + ':/home/bonobo/app',)
                command = "bin/bonobo run --install app"
            elif os.path.isfile(target):
                site_volumes += ('-v ' + os.path.dirname(target) + ':/home/bonobo/app',)
                command = "bin/bonobo run app/" + os.path.basename(target)
            else:
                raise IOError(
                    'File does not exist, or is of unsupported type (only directories and regular files are supported).'
                )
        elif module:
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
