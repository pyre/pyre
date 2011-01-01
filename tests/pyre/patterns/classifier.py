#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Verify that the AttributeClassifier works as advertised
"""


def test():
    # get the classifier
    from pyre.patterns.AttributeClassifier import AttributeClassifier

    # here are some descriptors
    class descriptor: pass
    class component(descriptor): pass
    class property(descriptor): pass

    class behavior(descriptor):
        def __init__(self, func): return

    # here is the metaclass
    class meta(AttributeClassifier):

        def __new__(cls, name, bases, attributes):
            attributes["traits"] = list(cls.pyre_harvest(attributes, descriptor))
            return super().__new__(cls, name, bases, attributes)


    # declare the containg class
    class base(metaclass=meta):

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
    assert base.traits == [ base.p1, base.c1, base.can, base.c2, base.p2, base.will ]

    return base


# main
if __name__ == "__main__":
    test()


# end of file 
