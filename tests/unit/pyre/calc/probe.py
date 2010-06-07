#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Verify that probes get notified when the values of their nodes change
"""


import pyre.calc


# make a probe that records the values of the monitored nodes
from pyre.calc.Probe import Probe
class Recorder(Probe):

    def activate(self, node):
        self.nodes[node] = node.value
        return

    def __init__(self, **kwds):
        super().__init__(**kwds)
        self.nodes = {}
        return


# tuck all the object references in a function so they get a chance to go out of scope
def test():
    # make a probe
    probe = Recorder()

    # make a node
    v = 80.
    production = pyre.calc.newNode(value=v)

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

    # shut the probe down
    probe.finalize()

    return


# main
if __name__ == "__main__":
    # get the extent manager
    from pyre.patterns.ExtentAware import ExtentAware
    # install it
    pyre.calc._metaclass_Node = ExtentAware
    # run the test
    test()
    # verify reference counts
    from pyre.calc.Node import Node
    # print(tuple(Node._pyre_extent))
    assert tuple(Node._pyre_extent) == ()


# end of file 
