#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Verify that the AttributeClassifier works as advertised
"""


def test():
    # get the classifier
    from pyre.patterns.AttributeClassifier import AttributeClassifier

    # here are some descriptors
    class component(AttributeClassifier.pyre_Descriptor): pass
    class property(AttributeClassifier.pyre_Descriptor): pass

    class behavior(AttributeClassifier.pyre_Descriptor):
        def __init__(self, func): return


    # declare the containg class
    class base(metaclass=AttributeClassifier, descriptors="traits", categories="index"):

        p1 = property()
        c1 = component()

        @behavior
        def can(self): pass

        c2 = component()
        p2 = property()

        @behavior
        def will(self): pass

    # now verify that it all happened correctly
    assert len(base.traits) == 6
    assert base.traits == ( base.p1, base.c1, base.can, base.c2, base.p2, base.will )

    return base


# main
if __name__ == "__main__":
    test()


# end of file 
