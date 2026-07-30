#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
The requirements trait converts text specifications into structured requirements
"""


def test():
    """
    Declare a component with a requirements trait and verify the coercion
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

    # instantiate
    consumer = Consumer(name="requirements_trait_consumer")
    # deposit text specifications
    consumer.reqs = ["hdf5>=1.12", "mpi[openmpi]"]
    # read the trait back
    reqs = consumer.reqs
    # both entries arrive
    assert len(reqs) == 2
    # as structured requirements
    assert all(isinstance(req, pyre.externals.requirement) for req in reqs)
    # with their sections harvested
    assert reqs[0].category == "hdf5" and reqs[0].clauses == ((">=", "1.12"),)
    assert reqs[1].category == "mpi" and reqs[1].selectors == ("openmpi",)

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
