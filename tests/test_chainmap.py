from typing import Any
import pytest
import chainmapping


def test_get_simple():
    dct = chainmapping.ChainMapping({"2": 3})
    assert dct["2"] == 3

def test_len():
    dct = chainmapping.ChainMapping({"2": 3}, {"2": 4, "3": 4}, {"3": 5, "4": 5})
    assert len(dct) == 3

def test_iter():
    dct = chainmapping.ChainMapping({"2": 3}, {"2": 4, "3": 4}, {"3": 5, "4": 5})
    got = set([k for k in dct])
    assert got == set(["2", "3", "4"])


def test_in():
    dct = chainmapping.ChainMapping({"2": 3}, {"2": 4, "3": 4}, {"3": 5, "4": 5})
    assert "2" in dct
    assert "3" in dct
    assert "4" in dct
    assert "5" not in dct


def test_true():
    dct: chainmapping.ChainMapping[Any, Any] = chainmapping.ChainMapping()
    assert bool(dct) is False
    dct = dct.new_child({})
    assert bool(dct) is False
    dct = dct.new_child({})
    assert bool(dct) is False
    dct = dct.new_child({2:3})
    assert bool(dct)
    dct = dct.new_child({})
    assert bool(dct)

    

def test_get_raises():
    dct = chainmapping.ChainMapping({"2": 3})
    with pytest.raises(KeyError):
        dct["3"]

def test_empty_map():
    dct: chainmapping.ChainMapping[Any, Any] = chainmapping.ChainMapping()
    assert dct.get(2, None) is None
    dct = dct.new_child({2: 3})
    assert dct.get(2, None) == 3

def test_get_default():
    dct = chainmapping.ChainMapping({"2": 3})
    assert dct.get("3") is None
    assert dct.get("3", 4) == 4