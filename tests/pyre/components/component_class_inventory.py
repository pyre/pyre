# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Exercise the various ways traits can pick up their default values
"""

import pyre


def declare(baseFamily=None, baseDefault=0, derivedFamily=None, derivedDefault=""):
    """
    Declare a pair of components
    """
    # the declaration
    class base(pyre.component, family=baseFamily):
        """a component"""
        bprop = pyre.properties.int(default=baseDefault)


    class derived(base, family=derivedFamily):
        """a derived component"""
        dprop = pyre.properties.str(default=derivedDefault)

    # return the pair to the caller
    return base, derived


def test():

    # build a pair without family names
    base, derived = declare()
    # check
    assert base.bprop == 0
    assert derived.bprop == 0
    assert derived.dprop == ""

    # now modify the base class property
    base.bprop = 1
    # check again
    assert base.bprop == 1
    assert derived.bprop == 1
    assert derived.dprop == "" # no cross-talk

    # build a pair with family names that match the sample configuration file
    base, derived = declare(
        baseFamily="sample.inventory.base",
        derivedFamily="sample.inventory.derived")
    # check
    assert base.bprop == 1
    assert derived.bprop == 2
    assert derived.dprop == "Hello world!"

    # modify the base class property
    base.bprop = 0
    # check
    assert base.bprop == 0
    assert derived.bprop == 2
    assert derived.dprop == "Hello world!"

    # adjust the string property
    derived.dprop = "{sample.file}"
    # and check
    assert derived.dprop == "sample.pml"

    return declare


# main
if __name__ == "__main__":
    test()


# end of file 
