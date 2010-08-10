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

    class sample(Component):
        """a representation of a gaussian function"""

        # properties
        energy = Property()
        energy.type = energy.schema.float()
        energy.default = 0.0
        energy.validators = energy.constraints.isPositive()

    # instantiate one
    s = sample(name="test")
    # attempt to set the trait to an illegal value
    try:
        s.energy = -1
        assert False
    except s.ConstraintViolationError as error:
        pass
    # all done
    return s


# main
if __name__ == "__main__":
    test()


# end of file 
