#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Exercise trait aliases
"""


import pyre


def declare():

    class gaussian(pyre.component, family="functor"):
        """a representation of a gaussian function"""

        # properties
        mean = pyre.properties.float(default="0.01")
        mean.aliases.add("μ")

        spread = pyre.properties.float(default="0.01")
        spread.aliases.add("σ")
       
        # behaviors
        @pyre.components.export
        def eval(self, x):
            return x
      
    return gaussian


def test():

    # print the store before the declaration
    # print(" -- at startup:")
    # cfg = pyre.executive.configurator
    # cfg.dump(pattern="(functor|gaussian)")
    # get the commandline slots
    # mean,_ = cfg._resolve(name='functor.μ')
    # print('functor.μ:')
    # mean.dump()
    # print(" -- done")

    gaussian = declare()
    # check that the aliases were properly registered
    assert gaussian.pyre_getTraitDescriptor("mean") == gaussian.pyre_getTraitDescriptor("μ")
    assert gaussian.pyre_getTraitDescriptor("spread") == gaussian.pyre_getTraitDescriptor("σ")
    # print out the configuration state
    # print(" -- after the declaration:")
    # print("gaussian: defaults: mean={0.mean!r}, spread={0.spread!r}".format(gaussian))
    # cfg.dump(pattern="(functor|gaussian)")
    # cfg._hash.dump()
    # print(" -- done")

    # check the class defaults
    # the values come from the defaults, functor.pml in this directory, and the command line
    assert gaussian.mean == 0.1
    assert gaussian.spread == 0.54
    # reset them to something meaningful
    gaussian.μ = 0.0
    gaussian.σ = 1.0
    # verify the change
    assert gaussian.mean == 0.0
    assert gaussian.spread == 1.0

    # instantiate one
    g = gaussian(name="gaussian")
    # make sure the defaults were transferred correctly
    assert g.mean == 0.56
    assert g.spread == 0.10
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
    # cfg.dump(pattern="(functor|gaussian)")

    return gaussian


# main
if __name__ == "__main__":
    test()


# end of file 
