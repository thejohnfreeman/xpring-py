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


## Updating the package for new definitions

When it comes time to publish a new version to handle new ledger types or
other updates to rippled, follow these steps:

1. Add at least one test transaction and confirm that they fail to serialize:

```shell
vim tests/test_definitions.py
poetry run invoke test
```

2. Update the rippled and xrpl.js dependencies:

```shell
cd submodules/rippled
git fetch origin
git merge --ff origin/develop
cd submodules/xrpl.js
git fetch origin
git merge --ff origin/main
```

3. Rebuild the protobuf definitions:

```shell
rm -rf xpring/proto/v1
poetry run invoke prebuild
```

4. Confirm that the tests now pass:

```shell
poetry run invoke test
```

5. Commit the changes:

```shell
git add --update .
git commit --message 'Migrate to definitions as of ...'
```

6. Bump the version:

```shell
poetry version patch
```

7. Commit the changes:

```shell
git add --update .
git commit --message 'Bump version to ...'
git tag v...
git push
git push --tags
```

8. Publish the updates:

```shell
poetry build
poetry publish --repository test
poetry publish
```
