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
        mean.default = "0.01"
        mean.aliases.add("μ")

        spread = Property()
        spread.default = "0.01"
        spread.aliases.add("σ")
       
        # behaviors
        @pyre.components.export
        def eval(self, x):
            return x
      
    # check that the aliases were properly registered
    assert gaussian.pyre_normalizeName("mean") == "mean"
    assert gaussian.pyre_normalizeName("μ") == "mean"
    assert gaussian.pyre_normalizeName("spread") == "spread"
    assert gaussian.pyre_normalizeName("σ") == "spread"
    # print out the configuration state
    # print("gaussian: defaults: mean={0.mean!r}, spread={0.spread!r}".format(gaussian))
    # calculator = pyre.executive().calculator
    # calculator._dump(pattern="(functor|gaussian)")
    # calculator._hash.dump()

    # check the class defaults
    # the values come from the defaults, functor.pml in this directory, and the command line
    assert gaussian.mean == '0.10'
    assert gaussian.spread == '0.54'
    # reset them to something meaningful
    gaussian.μ = 0.0
    gaussian.σ = 1.0
    # verify the change
    assert gaussian.mean == 0.0
    assert gaussian.spread == 1.0
    
    # instantiate one
    g = gaussian(name="gaussian")
    # make sure the defaults were transferred correctly
    assert g.mean == "0.56"
    assert g.spread == '0.10'
    # use the canonical names to reconfigure
    g.mean = 1.0
    g.spread = 2.0
    # check that access through the canonical name and the alias yield the same values
    assert g.μ == g.mean
    assert g.σ == g.spread
    # use the aliases to set
    g.μ = 0.0
    g.σ = 1.0
    # and check again
    assert g.μ == g.mean
    assert g.σ == g.spread

    # check the properties
    # print("g: mean={0.mean!r}, spread={0.spread!r}".format(g))
    # calculator._dump(pattern="(functor|gaussian)")

    return gaussian


# main
if __name__ == "__main__":
    test()


# end of file 
