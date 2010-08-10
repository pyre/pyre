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
    # here are some descriptors
    class trait(object): category = "traits"
    class component(object): category = "components"
    # and a function decorator
    def interface(func):
        func.category = "interfaces"
        return func

    # declare the containg class
    from pyre.patterns.AttributeClassifier import AttributeClassifier

    class base(object, metaclass=AttributeClassifier, classifier="category", index="index"):

        trait1 = trait()
        comp1 = component()

        @interface
        def can(self): pass

        comp2 = component()
        trait2 = trait()

        @interface
        def will(self): pass

    # now verify that it all happened correctly
    assert len(base.index) == 3
    assert base.index["traits"] == [ base.trait1, base.trait2 ]
    assert base.index["components"] == [ base.comp1, base.comp2 ]
    assert base.index["interfaces"] == [ base.can, base.will ]

    return base


# main
if __name__ == "__main__":
    test()


# end of file 
