#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a configuration file written by the pfg mill reads back: unset values come back
unset, lists come back with their entries, and tables with their keys
"""


def test() -> None:
    """
    Write the configuration of a component with the pfg mill, and read it back into another
    """
    # support
    import pyre

    # a component whose traits have defaults the file must override
    class Probe(pyre.component, family="pyre.tests.weaver.pfg.roundtrip.probe"):
        """
        A component with values of several kinds
        """

        # a moment
        stamp = pyre.properties.timestamp(default="2026-01-02T03:04:05")
        # a label
        label = pyre.properties.str(default="x")
        # a count
        count = pyre.properties.int(default=7)
        # a list of names
        names = pyre.properties.list(schema=pyre.properties.str(), default=["z"])
        # and a table
        table = pyre.properties.kv(default={"k": "v"})

    # make one
    original = Probe(name="original")
    # unset its scalars
    original.stamp = None
    original.label = None
    original.count = None
    # and give it new containers
    original.names = ["a", "b"]
    original.table = {"band": "L", "frequency": "A"}

    # make a weaver of configuration files
    weaver = pyre.weaver.weaver()
    # that writes pfg
    weaver.language = "pfg"
    # render the component
    document = original.pyre_renderTraitValues(renderer=weaver.language)
    # name the file after this test
    uri = "pfg_roundtrip.pfg"
    # a second component, configured by what the first one wrote, under a name of its own
    section = f"{original.pyre_spec}:"
    # open the file
    with open(uri, mode="w") as stream:
        # and write it
        for line in weaver.weave(document=document):
            # one line at a time, with the section of the original given to the copy
            print(line.replace(section, "pyre.tests.weaver.pfg.roundtrip.probe#copy:"), file=stream)

    # restoring is plain configuration
    pyre.loadConfiguration(uri)
    # build the copy
    copy = Probe(name="copy")

    # unset values come back unset: moments
    assert copy.stamp is None, repr(copy.stamp)
    # strings, rather than the text of {None}
    assert copy.label is None, repr(copy.label)
    # and numbers, rather than empty text an integer would refuse
    assert copy.count is None, repr(copy.count)
    # lists come back with their entries
    assert copy.names == ["a", "b"], repr(copy.names)
    # and tables with their keys
    assert dict(copy.table) == {"band": "L", "frequency": "A"}, repr(copy.table)

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
