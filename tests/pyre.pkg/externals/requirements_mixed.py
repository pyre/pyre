#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Text and structured requirements mix freely in one trait value
"""


def test():
    """
    Assign a list that mixes representations and verify uniform structured results
    """
    # support
    import pyre
    import pyre.externals

    # a component with a requirements trait
    class Consumer(pyre.component):
        """
        A component that depends on external packages
        """

        # the package requirements
        reqs = pyre.externals.requirements()
        reqs.doc = "the package requirements"

    # a structured requirement
    structured = pyre.externals.requirement.parse("hdf5[parallel]")
    # instantiate
    consumer = Consumer(name="requirements_mixed_consumer")
    # deposit a mix of text and structure
    consumer.reqs = [structured, "mpi[openmpi]"]
    # read the trait back
    reqs = consumer.reqs
    # both entries arrive
    assert len(reqs) == 2
    # the structured one passed through
    assert reqs[0].category == "hdf5" and reqs[0].selectors == ("parallel",)
    # and the text one was parsed
    assert reqs[1].category == "mpi" and reqs[1].selectors == ("openmpi",)

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
