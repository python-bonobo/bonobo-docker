import os


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