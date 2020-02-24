import typing as t

Test = t.Callable[..., t.Any]


class Mark:

    def skip(self, test: Test) -> Test:
        ...

    def parametrize(
        self,
        names: t.Union[str, t.Iterable[str]],
        arguments: t.Iterable[t.Any],
        ids: t.Iterable[str] = None,
    ) -> t.Callable[[Test], Test]:
        ...

    def xfail(self, test: Test) -> Test:
        ...


def param(*args: t.Any, id: str = None):
    ...


mark: Mark
