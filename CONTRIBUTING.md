## Dependencies

The protocol buffers and definitions file are in submodules:

```shell
git submodule update --init
```

Use [Poetry][] to install dependencies, build the protocol buffers,
and copy the definitions file:

```shell
poetry install --extras py
poetry run invoke prebuild
```

[Poetry]: https://python-poetry.org/docs/


## Tasks

There are several [Invoke][] tasks:

[Invoke]: http://www.pyinvoke.org/


```shell
poetry run invoke ${task}
```

- ``test``: [Pytest][] with coverage and doctests.
- ``lint``: [Mypy][], [Pylint][], and [Pydocstyle][].
- ``serve``: Serve the docs locally and rebuild them on file changes.

[Pytest]: https://docs.pytest.org/
[Mypy]: https://mypy.readthedocs.io/
[Pylint]: https://www.pylint.org/
[Pydocstyle]: http://www.pydocstyle.org/
