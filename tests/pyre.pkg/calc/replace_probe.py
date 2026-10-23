#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a node that replaces another inherits its observers, probes included
"""


# tuck all the object references in a function so they get a chance to go out of scope
def test():
    # access the package
    import pyre.calc

    # a probe is an observer
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

    # make a node
    u = pyre.calc.var(value="u")
    # another
    v = pyre.calc.var(value="v")
    # and one more that will replace {u}
    w = pyre.calc.var(value="w")
    # an operator that depends on {u}
    s = u + v
    # and a reference to {u}
    r = u.ref()

    # as we are, {u} has two observers: {s} and {r}
    assert identical(u.observers, {r, s})

    # make a probe
    p = probe()
    # ask it watch {u} and its dependents
    p.observe(observables=(u, s, r))

    # with the probe in place, {u} has three observers: {s}, {r}, and {p}
    assert identical(u.observers, {r, s, p})

    # {w} should have no observers
    assert identical(w.observers, set())
    # make the substitution
    w.replace(u)
    # {w} should have three observers: {s}, {r}, and {p}
    assert identical(w.observers, {p, s, r})

    # all done
    return


def identical(s1, s2):
    """
    Verify that the nodes in {s1} and {s2} are identical. This has to be done carefully since
    we must avoid triggering __eq__
    """
    # realize the first one
    s1 = tuple(s1)
    # and the second
    s2 = tuple(s2)
    # fail if their lengths are not the same
    if len(s1) != len(s2):
        # by reporting a mismatch
        return False
    # go through one
    for n1 in s1:
        # and the other
        for n2 in s2:
            # if this is a match, we are done
            if n1 is n2:
                # so move on to the next node
                break
        # if we didn't find n1 in s2
        else:
            # fail
            return False
    # if we get this far, all is good
    return True


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
