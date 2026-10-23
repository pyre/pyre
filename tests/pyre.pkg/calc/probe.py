#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that probes get notified when the values of their nodes change
"""


# tuck all the object references in a function so they get a chance to go out of scope
def test():
    # access the package
    import pyre.calc

    # get the base class
    from pyre.calc.Probe import Probe

    # make a probe that records the values of the monitored nodes
    class probe(Probe):
        """
        A probe that remembers the latest value of each node it watches
        """

        def flush(self, observable):
            """
            Record the value of {observable}, which just changed
            """
            # record the value of the node that changed
            self.nodes[observable] = observable.value
            # all done
            return self

        def __init__(self, **kwds):
            """
            Make a probe with no recorded values
            """
            # chain up
            super().__init__(**kwds)
            # start out with no recorded values
            self.nodes = {}
            # all done
            return

    # make a probe
    probe = probe()

    # pick a value
    v = 80.0
    # make a node that holds it
    production = pyre.calc.var(value=v)
    # verify the node has the value
    assert production.value == v

    # insert the probe
    probe.observe(observables=[production])

    # set the value
    production.value = v
    # check the node has it
    assert production.value == v
    # and the probe was told about it
    assert probe.nodes[production] == v

    # once more, with a new value
    v = 100.0
    # hand it to the node
    production.value = v
    # check the node has it
    assert production.value == v
    # and the probe was told about it
    assert probe.nodes[production] == v

    # all done
    return


# main
if __name__ == "__main__":
    # request debugging support for the pyre.calc package
    pyre_debug = {"pyre.calc"}
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()
    # verify reference counts
    from pyre.calc.Node import Node

    # no node outlives the test
    assert tuple(Node.pyre_extent) == ()


# end of file
