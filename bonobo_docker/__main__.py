import argparse
import re

import requests

from bonobo_docker import images, settings
from bonobo_docker.utils import run_docker

VERSION_RE = re.compile('bonobo-((?:[\d]+\.)+[\d+])-')


class BaseCommand:
    def __init__(self, parser):
        self.init(parser)

    def init(self, parser):
        pass

    def __call__(self, *args, **kwargs):
        return self.call(*args, **kwargs)

    def call(self, *args, **kwargs):
        raise NotImplementedError('Abstract.')


class BuildCommand(BaseCommand):
    def init(self, parser):
        parser.add_argument(
            '--version',
            '-v',
        )
        parser.add_argument('--push', '-p', action='store_true')
        parser.add_argument('--no-cache', action='store_true')

    def call(self, version=None, push=False, no_cache=False):
        # role : build docker images for bonobo
        # xxx todo add cache

        html = requests.get('https://pypi.python.org/simple/bonobo/')
        versions = list(sorted(set(VERSION_RE.findall(html.text)), key=lambda s: list(map(int, s.split('.')))))

        if version is None:
            version = versions[-1]

        if version not in versions:
            raise RuntimeError('Unknown version {}.'.format(version))

        tag, tags = version, {version}

        if version == versions[-1]:
            tags.add('latest')

        while '.' in tag:
            tag = tag[:tag.rfind('.')]
            matching_versions = list(filter(lambda x: x.startswith(tag), versions))

            if version == matching_versions[-1]:
                tags.add(tag)
            else:
                break

        tags = list(sorted(tags))

        run_docker(
            'build',
            *(['--no-cache'] if no_cache else []), '--build-arg BONOBO_VERSION={}'.format(version),
            *('-t {}:{}'.format(settings.IMAGE, tag) for tag in tags), images.__path__[0]
        )

        if push:
            for tag in tags:
                run_docker('push {}:{}'.format(settings.IMAGE, tag))


COMMANDS = {'build': BuildCommand}


def entrypoint(args=None):
    """
    Entrypoint for python -m bonobo-docker command. Only used for image plumbery and should not be userland
    """
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True

    commands = {}

    for name, command in COMMANDS.items():
        subparser = subparsers.add_parser(name)
        commands[name] = command(subparser)

    args = parser.parse_args(args).__dict__
    commands[args.pop('command')](**args)


if __name__ == '__main__':
    entrypoint()
