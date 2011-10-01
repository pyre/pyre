#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Verify that probes get notified when the values of their nodes change
"""


# tuck all the object references in a function so they get a chance to go out of scope
def test():
    import pyre.calc

    # make a probe that records the values of the monitored nodes
    from pyre.calc.Probe import Probe
    class Recorder(Probe):

        def flush(self, node):
            self.nodes[node] = node.value
            return

        def __init__(self, **kwds):
            super().__init__(**kwds)
            self.nodes = {}
            return

    # make a probe
    probe = Recorder()

    # make a node
    v = 80.
    production = pyre.calc.var(value=v)
    assert production.value == v

    # insert the probe
    probe.insert(production)

    # set and check the value
    production.value = v
    assert production.value == v
    assert probe.nodes[production] == v
    
    # once more
    v = 100.
    production.value = v
    assert production.value == v
    assert probe.nodes[production] == v

    return


# main
if __name__ == "__main__":
    # request debugging support for the pyre.calc package
    pyre_debug = { "pyre.calc" }
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()
    # verify reference counts
    from pyre.calc.Node import Node
    # print(tuple(Node._pyre_extent))
    assert tuple(Node._pyre_extent) == ()


# end of file 
