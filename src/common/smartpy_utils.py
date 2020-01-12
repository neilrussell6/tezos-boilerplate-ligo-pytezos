"""Common SmartPy Utils"""
import os
import subprocess
from functools import partial
from os.path import dirname, join

from src.common.path_utils import splitall
from src.common.pytest_utils import cached


def compile_smartpy_to_smlse(output_name, contract_cls, target_dir, *args, **kwargs):
    """Compile from SMLSE to Michelson and Micheline and return Micheline path."""
    contract = contract_cls(*args, **kwargs)
    target_smlse = join(target_dir, '_{}.smlse'.format(output_name))
    open(target_smlse, 'w').write(contract.export())
    return target_smlse


def compile_smlse_to_michelson_and_micheline(output_name, target_smlse, target_dir):
    """Compile from SMLSE to Michelson and Micheline and return Micheline path."""
    command = ['node', os.environ['SMARTPY_BASIC_JS_PATH']]
    for (opt, arg) in [('--compile', target_smlse), ('--outputDir', target_dir)]:
        command += [opt, arg]
    subprocess.run(command)
    return '_{}.tz'.format(output_name)


def _compile_smartpy_to_micheline(target_dir, output_name, contract_cls, file_path, *args, **kwargs):
    """Compile from SmartPy to Micheline and return Micheline path."""
    smlse_path = compile_smartpy_to_smlse(output_name, contract_cls, target_dir, *args, **kwargs)
    micheline_path = compile_smlse_to_michelson_and_micheline(output_name, smlse_path, target_dir)
    return join(dirname(file_path), micheline_path)


def compile_smartpy_to_micheline(output_name, contract_cls, file_path, cache=None, *args, **kwargs):
    """Compile from SmartPy to Micheline and return Micheline path or return cached Micheline path."""
    target_dir = dirname(file_path)
    f = partial(_compile_smartpy_to_micheline, target_dir, output_name, contract_cls, file_path, *args, **kwargs)
    if cache is None:
        return f()
    cache_key = '/'.join(splitall(file_path)[-4:]).replace('.py', '')
    return cached(cache, cache_key, f)
