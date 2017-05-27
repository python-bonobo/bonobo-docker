import os


def run_docker(*args):
    cmd = ' '.join(('docker', ) + args)
    print(cmd)
    return os.system(cmd)
