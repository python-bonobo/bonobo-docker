import inspect


def test_wildcard_import():
    bbdocker = __import__('bonobo_docker')
    assert bbdocker.__version__

    for name in dir(bbdocker):
        # ignore attributes starting by underscores
        if name.startswith('_'):
            continue
        attr = getattr(bbdocker, name)
        if inspect.ismodule(attr):
            continue

        assert name in bbdocker.__all__
