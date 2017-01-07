import argparse
import os

from bonobo_docker.services import client


def register(parser):
    parser.add_argument('file', type=argparse.FileType())
    return execute


def execute(file):
    """
    :param file file:
    :return:
    """
    container = client.containers.run(
        "bonobo-runtime:3.6",
        command="bin/python -m bonobo.commands run src/script.py",
        user='bonobo',
        detach=True,
        volumes={os.path.join(os.getcwd(), file.name): {
            'bind': '/home/bonobo/src/script.py',
            'mode': 'ro'
        }}
    )
    for line in container.logs(stream=True):
        print(line.decode('utf-8'), end='')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    command = register(parser)
    args = parser.parse_args()
    command(**args.__dict__)
