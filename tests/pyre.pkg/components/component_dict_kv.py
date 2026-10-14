#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a {kv} trait is a table of strings that behaves like a dictionary: its defaults,
the operations clients use to read it, and the independence of the tables of different
instances
"""


def test() -> None:
    """
    Read and compare {kv} tables the way clients do
    """
    # support
    import collections.abc
    import pickle
    import pyre

    # a component with tables
    class Reader(pyre.component, family="pyre.tests.dict.kv.reader"):
        """
        A component with {kv} traits
        """

        # a table with the default default
        selection = pyre.properties.kv()
        # and one with a default of its own
        labels = pyre.properties.kv(default={"band": "L"})

    # get the traits
    selection = Reader.pyre_trait("selection")
    labels = Reader.pyre_trait("labels")
    # a {kv} is a dict of strings
    assert selection.type == "dict[str]"
    # whose default is an empty table
    assert selection.default == {}
    # unless it was given one
    assert labels.default == {"band": "L"}

    # make two readers
    one = Reader(name="one")
    two = Reader(name="two")
    # both start with the defaults
    assert dict(one.selection) == {} and dict(two.selection) == {}
    assert dict(one.labels) == {"band": "L"} and dict(two.labels) == {"band": "L"}

    # change a key of one of them
    one.labels["band"] = "S"
    # and add another
    one.labels["frequency"] = "A"
    # which leaves the other alone
    assert dict(two.labels) == {"band": "L"}
    # as well as the default of the trait
    assert labels.default == {"band": "L"}

    # the table is a mapping
    table = one.labels
    assert isinstance(table, collections.abc.Mapping)
    # with a size
    assert len(table) == 2
    # that knows its keys
    assert "band" in table and "polarization" not in table
    # can be read by key
    assert table["band"] == "S"
    # with a fallback for missing keys
    assert table.get("polarization") is None and table.get("polarization", "HH") == "HH"
    # can be traversed
    assert sorted(table) == ["band", "frequency"]
    assert sorted(table.keys()) == ["band", "frequency"]
    assert sorted(table.values()) == ["A", "S"]
    assert sorted(table.items()) == [("band", "S"), ("frequency", "A")]
    # compares equal to a dictionary with the same contents
    assert table == {"band": "S", "frequency": "A"}
    # and can be turned into one, by itself or merged with others
    assert dict(table) == {"band": "S", "frequency": "A"}
    assert {**dict(two.labels), **dict(table)} == {"band": "S", "frequency": "A"}
    # it merges the way dictionaries do
    assert two.labels | table == {"band": "S", "frequency": "A"}
    assert {"polarization": "HH"} | table == {"polarization": "HH", "band": "S", "frequency": "A"}
    # prints like one
    assert repr(table) == repr({"band": "S", "frequency": "A"})
    # copies into one
    assert type(table.copy()) is dict and table.copy() == {"band": "S", "frequency": "A"}
    # and pickles as one, since the slots of its entries stay behind
    assert pickle.loads(pickle.dumps(table)) == {"band": "S", "frequency": "A"}
    # reading a missing key fails the way it does for a dictionary
    try:
        # so asking for one
        table["polarization"]
        # must fail
        assert False, "a missing key was found"
    # with a key error
    except KeyError:
        # as expected
        pass

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
