#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Exercise component inheritance
"""


def test():
    # access
    from pyre.components.Property import Property
    from pyre.components.Component import Component

    # declare an component
    class base(Component):
        """a base component"""
        # traits
        common = Property()
        common.default = "base.common"

    # and derive another from it
    class derived(base):
        """a derived component"""
        # traits
        extra = Property()
        extra.default = "derived.extra"

    # check that the defaults are readable
    assert base.common == "base.common"
    assert derived.common == "base.common"
    assert derived.extra == "derived.extra"
    # check that the defaults are writable
    base.common = "base:common"
    derived.common = "base:common"
    derived.extra = "derived:extra"
    # check that the defaults were recorded properly
    assert base.common == "base:common"
    assert derived.common == "base:common"
    assert derived.extra == "derived:extra"

        
    return base, derived


# main
if __name__ == "__main__":
    test()


# end of file 
