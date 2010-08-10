#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Exercise component configuration in the presence of inheritance
"""


def declare():
    # access
    from pyre.components.Property import Property
    from pyre.components.Component import Component

    # declare a component
    class base(Component, family="sample.base"):
        """a base component"""
        # traits
        common = Property()
        common.default = "base"

    class intermediate(base):
        """an intermediate component in the hierarchy that doesn't declare a family"""
        # traits
        middle = Property()
        middle.default = "intermediate"

    # and derive another from it
    class derived(intermediate, family="sample.derived"):
        """a derived component"""
        # traits
        extra = Property()
        extra.default = "derived"

    return base, intermediate, derived


def test():
    import pyre
    import pyre.filesystem
    # build a filesystem for this directory
    local = pyre.filesystem.newLocalFilesystem('.')
    # get the executive
    pyx = pyre.executive()
    # and its fileserver
    fs = pyx.fileserver
    # mount the current directory as 'local'
    fs['local'] = local
    # add it to the config path
    pyx.configpath.append('vfs:///local')

    # get the declarations
    base, intermediate, derived = declare()

    # check the defaults
    inventory = base._pyre_Inventory
    assert inventory.common.value == "base - common"
        
    inventory = intermediate._pyre_Inventory
    assert inventory.common.value == "base - common"
    assert inventory.middle.value == "intermediate"

    inventory = derived._pyre_Inventory
    assert inventory.extra.value == "derived - extra"
    assert inventory.middle.value == "intermediate"
    assert inventory.common.value == "derived - common"

    # make the components available
    return base, intermediate, derived


# main
if __name__ == "__main__":
    test()


# end of file 
