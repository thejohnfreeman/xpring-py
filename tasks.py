from invoke import task
import multiprocessing
from pathlib import Path
import sys
import toml

pty = sys.stdout.isatty()


def get_package_name() -> str:
    pyproject = toml.load(open('pyproject.toml', 'r'))
    return pyproject['tool']['poetry']['name']


@task
def proto(c):
    # protoc does not let us prefix the package for protobufs,
    # so we use this workaround.
    # https://github.com/protocolbuffers/protobuf/issues/1491

    src_dir = 'xpring-common-protocol-buffers/proto'
    dst_dir = 'xpring/proto'
    # Doctest imports each module independently, with no parent package,
    # which breaks relative imports. Thus, we must use absolute imports.
    # package = '.'
    package = 'xpring.proto'

    Path(dst_dir).mkdir(exist_ok=True)
    c.run(
        f'python -m grpc_tools.protoc --proto_path={src_dir} --python_out={dst_dir} --grpc_python_out={dst_dir} {src_dir}/*.proto'
    )
    c.run(f"sed -i -E 's/^import.*_pb2/from {package} \\0/' {dst_dir}/*.py")


@task
def lint(c):
    package_name = get_package_name()
    nproc = multiprocessing.cpu_count()
    c.run(f'mypy {package_name} tests', echo=True, pty=pty)
    c.run(f'pylint --jobs {nproc} {package_name} tests', echo=True, pty=pty)
    c.run(f'pydocstyle {package_name} tests', echo=True, pty=pty)


@task
def test(c):
    package_name = get_package_name()
    c.run(
        f'pytest --cov={package_name} --ignore=docs --ignore=tasks.py --doctest-modules',
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
