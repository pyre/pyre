#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Malformed requirements in a trait value are reported, not silently dropped
"""


def test():
    """
    Assign a list with a broken specification and verify the failure is loud
    """
    # support
    import pyre
    import pyre.externals

    # get the casting error the type system raises
    from pyre.schemata.exceptions import CastingError

    # a component with a requirements trait
    class Consumer(pyre.component):
        """
        A component that depends on external packages
        """

        # the package requirements
        reqs = pyre.externals.requirements()
        reqs.doc = "the package requirements"

    # instantiate
    consumer = Consumer(name="requirements_errors_consumer")
    # deposit a list with a malformed entry
    consumer.reqs = ["hdf5>=1.12", "mpi[]"]
    # attempt to
    try:
        # read the trait back
        consumer.reqs
    # the broken entry must be reported
    except CastingError:
        # as expected
        pass
    # a generic sequence would have dropped it silently, leaving one requirement behind
    else:
        # which subverts the resolver
        assert False, "a malformed requirement went unreported"

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
