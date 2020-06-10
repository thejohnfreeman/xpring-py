import fileinput
import glob
import multiprocessing
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile

from invoke import task
import toml

pty = sys.stdout.isatty()


def get_package_name() -> str:
    pyproject = toml.load(open('pyproject.toml', 'r'))
    return pyproject['tool']['poetry']['name']


# We can assume Python is in the environment, but not sed.
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

    import_dir = Path('submodules/rippled/src/ripple/proto')
    # The sources *must* reside within the import directory.
    # When protoc runs, it recreates the relative directory structure.
    # In other words, the source `{import_dir}/rpc/v1/tx.proto`
    # will generate a source `{dst_dir}/rpc/v1/tx_pb2.py`.
    source_dir = Path('submodules/rippled/src/ripple/proto/org/xrpl/rpc/v1')
    dst_dir = Path('xpring/proto/v1')

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_dir = Path(tmp_dir)

        c.run(
            f'python -m grpc_tools.protoc --proto_path={import_dir} '
            f'--python_out={tmp_dir} '
            f'--grpc_python_out={tmp_dir} '
            f'--mypy_out=quiet:{tmp_dir} '
            f'{source_dir}/*.proto'
        )

        prefix = source_dir.relative_to(import_dir)
        package_prefix = str(prefix).replace(os.sep, '.')

        # Change absolute imports of sibling protobufs to relative imports
        # because the protobufs are nested under package `xpring.proto.v1`.
        # prefix empty: import type_pb2
        substitute(f'{tmp_dir}/**/*.py', '^import.*_pb2', 'from . \g<0>')
        # prefix not empty: from package.prefix import type_pb2
        substitute(f'{tmp_dir}/**/*.py', f'^from\s+{package_prefix}', 'from .')
        # These next two substitutions interact. They must be executed together.
        # prefix not empty: from package.prefix.type_pb2 import
        substitute(
            f'{tmp_dir}/**/*.pyi', f'^from\s+{package_prefix}\.', 'from '
        )
        # prefix empty: from type_pb2 import
        substitute(f'{tmp_dir}/**/*.pyi', '^from\s+(\S+_pb2)', 'from .\g<1>')
        # https://github.com/dropbox/mypy-protobuf/issues/116
        substitute(f'{tmp_dir}/**/*.pyi', '(\S+\s*)global___', '\g<1>')

        Path(dst_dir).mkdir(exist_ok=True)
        (tmp_dir / prefix).rename(dst_dir)
        (dst_dir / '__init__.py').touch()


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
