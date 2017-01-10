from .services import client


def runc():
    client.containers.run("ubuntu", "echo hello world")


if __name__ == '__main__':
    runc()
