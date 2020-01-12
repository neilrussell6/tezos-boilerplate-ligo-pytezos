import pytest
from shutil import rmtree
from os import mkdir


@pytest.yield_fixture(autouse=True, scope='session')
def clear_cache(request):
    rmtree(request.config.cache._cachedir)
    mkdir(request.config.cache._cachedir)
    yield
