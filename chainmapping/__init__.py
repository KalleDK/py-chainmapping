from typing import Mapping, Optional, TypeVar, Union, overload

_Key_T = TypeVar("_Key_T")
_Value_U = TypeVar("_Value_U")
_Default_V = TypeVar("_Default_V")


class ChainMapping(Mapping[_Key_T, _Value_U]):
    """A ChainMap groups multiple dicts (or other mappings) together
    to create a single, readonly view.

    The underlying mappings are stored in a list.  That list is public and can
    be accessed or updated using the *maps* attribute.  There is no other
    state.

    Lookups search the underlying mappings successively until a key is found.


    """

    def __init__(self, *maps: Mapping[_Key_T, _Value_U]):
        """Initialize a ChainMap by setting *maps* to the given mappings.
        If no mappings are provided, a single empty dictionary is used.

        """
        self.maps = maps

    def __missing__(self, key: _Key_T):
        raise KeyError(key)

    def __getitem__(self, key: _Key_T):
        for mapping in self.maps:
            try:
                return mapping[key]  # can't use 'key in mapping' with defaultdict
            except KeyError:
                pass
        return self.__missing__(key)  # support subclasses that define __missing__

    @overload
    def get(self, key: _Key_T, default: None = ...) -> Optional[_Value_U]:  # pragma: no cover
        ...

    @overload
    def get(self, key: _Key_T, default: _Default_V) -> Union[_Value_U, _Default_V]:  # pragma: no cover
        ...

    def get(self, key: _Key_T, default: _Default_V | None = None) -> Union[_Default_V, _Value_U, None]:
        return self[key] if key in self else default

    def new_child(self, map: Mapping[_Key_T, _Value_U]):
        return ChainMapping(map, *self.maps)

    def __len__(self):
        s: set[_Key_T] = set()
        return len(s.union(*self.maps))  # reuses stored hash values if possible

    def __iter__(self):
        d: dict[_Key_T, None] = {}
        for mapping in reversed(self.maps):
            d.update(dict.fromkeys(mapping))  # reuses stored hash values if possible
        return iter(d)

    def __contains__(self, key: object):
        return any(key in m for m in self.maps)

    def __bool__(self):
        return any(self.maps)
