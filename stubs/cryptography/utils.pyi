import typing as t


def register_interface(interface: t.Any) -> t.Callable[[t.Any], None]:
    ...
