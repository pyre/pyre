#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Verify that the trait defaults get bound correctly from the configuration store
"""


def test():
    import pyre

    # declare an interface
    class job(pyre.interface):
        """an interface"""
        @pyre.provides
        def do(self):
            """do something"""

    # declare a component the implements this interface
    class worker(pyre.component, family="sample.worker", implements=job):
        """an implementation"""
        host = pyre.properties.str(default="localhost")
        @pyre.export
        def do(self):
            """do something"""

    # declare a component
    class component(pyre.component, family="sample.manager"):
        """the base component"""
        jobs = pyre.properties.int(default=1)
        gopher = pyre.facility(interface=job, default=worker)
        @pyre.export
        def say(self):
            """say something"""

    # instantiate the component
    c = component(name="c")
    # check that the configuration settings were applied correctly
    assert c.jobs == 10
    assert isinstance(c.gopher, worker)
    assert c.gopher.pyre_name == "c.gopher"
    assert c.gopher.host == "foxtrot.caltech.edu"
    # instantiate the worker
    w = worker(name="w")
    assert w.host == "pyre.caltech.edu"
    # bind the two, which should cause some extra configuration of {w}
    # now that it is bound to {c.task}
    c.gopher = w
    # check that the binding caused the transfer of configuration settings
    assert c.gopher == w
    assert c.gopher.pyre_name == "w"
    assert c.gopher.host == "foxtrot.caltech.edu"

    return c


# main
if __name__ == "__main__":
    test()


# end of file 
