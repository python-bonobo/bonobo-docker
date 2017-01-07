from bonobo import Graph, tee, run, ThreadPoolExecutorStrategy
import pprint


def extract():
    yield 'foo'
    yield 'bar'
    yield 'baz'


def transform(x: str):
    return x.upper() + ' transformed'


exports = {
    'default': Graph(
        extract,
        transform,
        tee(pprint.pprint),
    )
}

executor = ThreadPoolExecutorStrategy()
executor.execute(exports['default'])
