#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Splitting a requirements string is grammar aware: conjunction commas don't sever entries
"""


def test():
    """
    Feed the trait text values whose version conjunctions contain the list delimiter
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
    consumer = Consumer(name="requirements_split_consumer")
    # deposit a single string whose first entry carries a version conjunction
    consumer.reqs = "hdf5>=1.12,<2, mpi[openmpi]"
    # read the trait back
    reqs = consumer.reqs
    # the conjunction comma did not sever the first entry
    assert len(reqs) == 2
    # the window survived intact
    assert reqs[0].category == "hdf5" and reqs[0].clauses == ((">=", "1.12"), ("<", "2"))
    # and the second entry is whole
    assert reqs[1].category == "mpi" and reqs[1].selectors == ("openmpi",)

    # a bracketed rendering splits the same way
    consumer.reqs = "[gsl>=2.8,!=2.9, python>=3.12]"
    # read it back
    reqs = consumer.reqs
    # both entries arrive
    assert len(reqs) == 2
    # with the conjunction intact
    assert reqs[0].clauses == ((">=", "2.8"), ("!=", "2.9"))
    # and the brackets stripped
    assert reqs[1].category == "python"

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
