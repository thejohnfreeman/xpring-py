import typing as t

Test = t.Callable[..., t.Any]


class Mark:

    def skip(self, test: Test) -> Test:
        ...

    def parametrize(self, names: str,
                    arguments: t.Iterable[t.Any]) -> t.Callable[[Test], Test]:
        ...


mark: Mark
