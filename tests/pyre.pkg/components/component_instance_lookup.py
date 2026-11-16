#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the registrar finds a component instance by name, that asking for a name again
hands back the same instance, that anonymous instances are not indexed by name, and that the
index does not keep an instance alive
"""


def test():
    """
    Look up component instances by name
    """
    # externals
    import gc
    import weakref

    # access the framework
    import pyre

    # declare a component
    class component(pyre.component, family="pyre.tests.lookup"):
        """a trivial component"""

        # a trait, so the instances have something to configure
        p = pyre.properties.int()

    # get the registrar
    registrar = component.pyre_registrar
    # make a named instance
    c = component(name="lookup.c")
    # the registrar finds it by name
    assert registrar.retrieveComponentByName(componentClass=component, name="lookup.c") is c
    # and asking for the name again hands back the same instance
    assert component(name="lookup.c") is c
    # a name nobody has taken finds nothing
    assert registrar.retrieveComponentByName(componentClass=component, name="lookup.d") is None

    # an anonymous instance is part of the extent
    a = component()
    # of the class
    assert a in set(component.pyre_getExtent())
    # but it has no name to be found by
    assert a.pyre_name is None
    # so it is not in the index
    assert a not in registrar.names[component].values()

    # watch the anonymous instance
    watcher = weakref.ref(a)
    # let go of it
    del a
    # and collect
    gc.collect()
    # it is gone, so neither the extent nor the index kept it alive
    assert watcher() is None

    # all done
    return c


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
