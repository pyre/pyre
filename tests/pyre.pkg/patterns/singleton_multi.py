#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Verify that multiple calls to a singleton constructor yield the same instance
    """
    # access
    from pyre.patterns.Singleton import Singleton

    # a singleton class
    class Host(metaclass=Singleton):
        """
        Information about this machine
        """

        # public data
        name = None

        # metamethods
        def __init__(self, name=name, **kwds):
            # chain yp
            super().__init__(**kwds)
            # set the name
            self.name = name
            # all done
            return

    # a hostname
    hostname = "fiji.para-sim.com"
    # instantiate
    fiji = Host(name=hostname)
    # check that it matches the singleton instance
    assert fiji is Host.pyre_singletonInstance
    # check that the name was registered correctly
    assert fiji.name == hostname

    # another access; not that we don't have to worry about the name of the host, or respect
    # the signature of the constructor for that matter
    alias = Host()
    # verify that this is the same instance
    assert alias is fiji
    # and that the names match
    assert alias.name is fiji.name

    # rename the host
    new = "amalfi.orthologue.com"
    # modify
    alias.name = new
    # verify that both changed
    assert fiji.name is new

    # all done
    return Host


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
