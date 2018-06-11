import argparse
import logging
import re

import requests
from semantic_version import Version

from bonobo_docker import images, settings
from bonobo_docker.logging import logger
from bonobo_docker.utils import run_docker

VERSION_RE = re.compile('bonobo-((?:[\d]+\.)+[\d+](?:(?:a|b|rc)[\d]+)?)-')


class BaseCommand:
    def __init__(self, parser):
        self.init(parser)

    def init(self, parser):
        pass

    def __call__(self, *args, **kwargs):
        return self.call(*args, **kwargs)

    def call(self, *args, **kwargs):
        raise NotImplementedError('Abstract.')


class PythonVersion(Version):
    version_re = re.compile(r'^(\d+)\.(\d+)\.(\d+)(?:([0-9a-zA-Z.-]+))?(?:\+([0-9a-zA-Z.-]+))?$')
    partial_version_re = re.compile(r'^(\d+)(?:\.(\d+)(?:\.(\d+))?)?(?:([0-9a-zA-Z.-]*))?(?:\+([0-9a-zA-Z.-]*))?$')

    def __str__(self):
        version = '%d' % self.major
        if self.minor is not None:
            version = '%s.%d' % (version, self.minor)
        if self.patch is not None:
            version = '%s.%d' % (version, self.patch)

        if self.prerelease or (self.partial and self.prerelease == () and self.build is None):
            version = '%s%s' % (version, '.'.join(self.prerelease))
        if self.build or (self.partial and self.build == ()):
            version = '%s+%s' % (version, '.'.join(self.build))
        return version


class BuildCommand(BaseCommand):
    def init(self, parser):
        parser.add_argument(
            '--version',
            '-v',
        )
        parser.add_argument('--push', '-p', action='store_true')
        parser.add_argument('--no-cache', action='store_true')
        parser.add_argument('--dry-run', action='store_true')

    def call(self, *, version=None, push=False, no_cache=False, dry_run=False):
        # role : build docker images for bonobo
        # xxx todo add cache

        html = requests.get('https://pypi.python.org/simple/bonobo/')
        versions = list(sorted(PythonVersion(v) for v in set(VERSION_RE.findall(html.text))))

        if version is None:
            version = versions[-1]
        else:
            version = PythonVersion(version)

        if version not in versions:
            raise RuntimeError('Unknown version {}.'.format(version))

        tag, tags = str(version), {str(version)}

        if version == versions[-1]:
            if version.prerelease:
                tags.add('edge')
            else:
                tags.add('latest')

        while '.' in tag:
            tag = tag[:tag.rfind('.')]
            matching_versions = list(filter(lambda x: str(x).startswith(tag), versions))

            if version == matching_versions[-1]:
                tags.add(tag)
            else:
                break

        tags = list(sorted(tags))

        docker_command = [
            'build', *(['--no-cache'] if no_cache else []), '--build-arg BONOBO_VERSION={}'.format(version),
            *('-t {}:{}'.format(settings.IMAGE, tag) for tag in tags), images.__path__[0]
        ]

        run_docker(*docker_command, dry_run=dry_run)

        if push:
            for tag in tags:
                run_docker('push {}:{}'.format(settings.IMAGE, tag), dry_run=dry_run)


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
    logger.setLevel(logging.INFO)
    entrypoint()
