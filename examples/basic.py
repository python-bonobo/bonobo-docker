from bonobo import Graph, tee
import pprint


def extract():
    yield 'foo'
    yield 'bar'
    yield 'baz'


def transform(x: str):
    return x.upper() + ' transformed'


graph = Graph(
    extract,
    transform,
    tee(pprint.pprint),
)

if __name__ == '__main__':
    from bonobo import console_run
    console_run(graph)
