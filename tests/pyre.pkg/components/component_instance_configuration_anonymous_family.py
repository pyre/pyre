#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that an anonymous instance takes the configuration of its family from a file, that its
constructor arguments override it, and that the configuration of a named instance of the same
family never reaches it
"""


def test() -> None:
    """
    Load a file that configures a family and one named instance, and build instances of both kinds
    """
    # support
    import pyre

    # a component with two traits
    class Filter(pyre.component, family="pyre.tests.anonymous.family.filter"):
        """
        A component with two strings
        """

        # the first
        begin = pyre.properties.str()
        begin.default = "default"
        # and the second
        end = pyre.properties.str()
        end.default = "default"

    # load the configuration file
    pyre.loadConfiguration("component_instance_configuration_anonymous_family.yaml")

    # an anonymous instance
    anonymous = Filter()
    # has no name
    assert anonymous.pyre_name is None
    # takes the configuration of the family, and nothing named
    assert (anonymous.begin, anonymous.end) == ("family", "default")
    # one built with a value
    built = Filter(begin="argument")
    # keeps the value over the configuration of the family
    assert (built.begin, built.end) == ("argument", "default")
    # the named instance
    coast = Filter(name="coast")
    # takes both the configuration of the family and its own
    assert (coast.begin, coast.end) == ("family", "coast")
    # and anonymous instances built after it
    later = Filter()
    # still take only the configuration of the family
    assert (later.begin, later.end) == ("family", "default")
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
