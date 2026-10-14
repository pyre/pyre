#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a dict trait is a property: it is listed with the properties of its component,
describes itself as one, and records a plain locator when one of its keys is set in the code
"""


def test() -> None:
    """
    Inspect a dict trait as a property
    """
    # support
    import pyre

    # a component with a table
    class Reader(pyre.component, family="pyre.tests.dict.property.reader"):
        """
        A component with a dict trait
        """

        # a table of strings
        selection = pyre.properties.kv()

    # get the trait
    selection = Reader.pyre_trait("selection")
    # it is a property
    assert selection.isProperty
    assert selection.category == "property"
    # so it is listed with the properties of its component
    assert [trait.name for trait in Reader.pyre_properties()] == ["selection"]
    # and describes itself as one
    assert str(selection) == "'selection': a property of type 'dict'"
    # it is the only property that holds a map: there are no typed properties of mappings
    assert not hasattr(pyre.properties.property, "mapping")
    assert not hasattr(pyre.properties.property, "catalog")
    # and a catalog is a dict of lists
    assert pyre.properties.catalog().type == "dict[list[str]]"

    # make a reader
    reader = Reader(name="reader")
    # set one of its keys in the code
    reader.selection["band"] = "L"
    # access the store
    nameserver = pyre.executive.nameserver
    # the entry says, in plain words, how it was set
    locator = nameserver.getInfo(nameserver.hash("reader.selection.band")).locator
    assert str(locator) == "while setting 'band' in 'selection'", str(locator)

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
