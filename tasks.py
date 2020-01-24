import fileinput
import glob
from invoke import task
import multiprocessing
from pathlib import Path
import re
import shutil
import sys
import toml

pty = sys.stdout.isatty()


def get_package_name() -> str:
    pyproject = toml.load(open('pyproject.toml', 'r'))
    return pyproject['tool']['poetry']['name']


def substitute(files: str, pattern: str, replacement: str):
    """A cross-platform approximation of `sed -i -E s/pattern/replacement/ files`."""
    with fileinput.input(
        files=glob.glob(files, recursive=True), inplace=True
    ) as file:
        for line in file:
            print(re.sub(pattern, replacement, line), end='')


@task
def proto(c):
    # protoc does not let us prefix the package for protobufs,
    # so we use this workaround.
    # https://github.com/protocolbuffers/protobuf/issues/1491

    src_dir = 'submodules/xpring-common-protocol-buffers/proto'
    dst_dir = 'xpring/proto'
    # Doctest imports each module independently, with no parent package,
    # which breaks relative imports. Thus, we must use absolute imports.
    # package = '.'
    package = 'xpring.proto'

    Path(dst_dir).mkdir(exist_ok=True)
    c.run(
        f'python -m grpc_tools.protoc --proto_path={src_dir} '
        f'--python_out={dst_dir} '
        f'--grpc_python_out={dst_dir} '
        f'--mypy_out=quiet:{dst_dir} '
        f'{src_dir}/*.proto'
    )
    # We can assume Python is in the environment, but not sed.
    substitute(f'{dst_dir}/*.py', '^import.*_pb2', 'from . \g<0>')
    substitute(f'{dst_dir}/*.pyi', '^from\s+(\S+_pb2)', 'from .\g<1>')


@task
def definitions(c):
    shutil.copy(
        'submodules/ripple-binary-codec/src/enums/definitions.json', 'xpring'
    )


@task(pre=[proto, definitions])
def prebuild(c):
    pass


@task
def mypy(c):
    package_name = get_package_name()
    c.run(
        f'mypy {package_name} tests',
        env={'MYPYPATH': 'stubs'},
        echo=True,
        pty=pty
    )


@task(pre=[mypy])
def lint(c):
    package_name = get_package_name()
    nproc = multiprocessing.cpu_count()
    c.run(f'pylint --jobs {nproc} {package_name} tests', echo=True, pty=pty)
    c.run(f'pydocstyle {package_name} tests', echo=True, pty=pty)


@task
def test(c):
    package_name = get_package_name()
    c.run(
        f'pytest --cov={package_name} --doctest-modules {package_name} tests',
        echo=True,
        pty=pty
    )


@task
def html(c):
    c.run('make -C docs html', echo=True, pty=pty)


@task
def serve(c):
    c.run(
        'sphinx-autobuild docs docs/_build/html --host 0.0.0.0 --watch .',
        echo=True,
        pty=pty
    )
