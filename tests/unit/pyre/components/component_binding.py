#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
A more elaborate component declaration
"""


import pyre


def test():
    from pyre.components.Component import Component
    from pyre.components.Property import Property

    class gaussian(Component, family="functor"):
        """a representation of a gaussian function"""

        # properties
        mean = Property()
        mean.type = mean.schema.float()
        mean.default = 0.0
        mean.aliases.add("μ")

        spread = Property()
        spread.type = mean.schema.float()
        spread.default = 1.0
        spread.aliases.add("σ")
       
        # behaviors
        @pyre.components.export
        def eval(self, x):
            return x
      
    # print out the configuration state
    # print("gaussian: defaults: mean={0.mean!r}, spread={0.spread!r}".format(gaussian))
    # calculator = pyre.executive().calculator
    # calculator._dump(pattern="(functor|gaussian)")

    # instantiate one
    g = gaussian(name="gaussian")
    # check the properties
    # print("g: mean={0.mean!r}, spread={0.spread!r}".format(g))
    # calculator = pyre.executive().calculator
    # calculator._dump(pattern="(gaussian)")

    # make sure the defaults were transferred correctly
    assert type(g.mean) == float
    assert g.mean == .56
    assert type(g.spread) == float
    assert g.spread == .58

    # make some assignments
    # from integers
    # print("assign an integer")
    g.mean = 1
    # print("done")
    assert type(g.mean) == float
    assert g.mean == 1.0
    # from strings
    # print("assign a string")
    g.mean = "1.0"
    # print("done")
    assert type(g.mean) == float
    assert g.mean == 1.0

    return gaussian


# main
if __name__ == "__main__":
    test()


# end of file 
