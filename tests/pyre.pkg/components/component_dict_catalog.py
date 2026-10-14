#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a {catalog}, a dict of lists, takes whole tables, lists one key at a time, and text
with one item per list
"""


def test() -> None:
    """
    Fill a catalog in the ways a client can
    """
    # support
    import pyre

    # access the store
    nameserver = pyre.executive.nameserver
    # a list for one key, in its text form, the way a configuration file would set it
    nameserver.insert(
        name="configured.languages.c++",
        value="clang++, g++",
        priority=nameserver.priority.user(),
        locator=pyre.tracking.simple("the test"),
    )

    # a component with a catalog
    class Toolbox(pyre.component, family="pyre.tests.dict.catalog.toolbox"):
        """
        A component with a catalog
        """

        # compilers, by language
        languages = pyre.properties.catalog()

    # a catalog is a dict of lists of strings
    assert Toolbox.pyre_trait("languages").type == "dict[list[str]]"

    # the list set for a key in the store
    assert dict(Toolbox(name="configured").languages) == {"c++": ["clang++", "g++"]}

    # make another toolbox
    toolbox = Toolbox(name="toolbox")
    # it starts out empty
    assert dict(toolbox.languages) == {}
    # assign a whole table
    toolbox.languages = {"c": ["clang", "gcc"], "fortran": ("gfortran",)}
    # and its values become lists
    assert dict(toolbox.languages) == {"c": ["clang", "gcc"], "fortran": ["gfortran"]}
    # set the list of one key from its text form
    toolbox.languages["cuda"] = "nvcc, clang"
    # and it is split into items
    assert toolbox.languages["cuda"] == ["nvcc", "clang"]
    # text for the whole table can hold one item per list, since commas separate its entries
    toolbox.languages = "c:gcc, fortran:gfortran"
    # each of which becomes a list
    assert dict(toolbox.languages) == {"c": ["gcc"], "fortran": ["gfortran"]}

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
