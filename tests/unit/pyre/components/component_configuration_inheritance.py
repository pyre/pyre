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

    # declare an component
    class base(Component, family="sample.base"):
        """a base component"""
        # traits
        common = Property()
        common.default = "base"

    # and derive another from it
    class derived(base, family="sample.derived"):
        """a derived component"""
        # traits
        extra = Property()
        extra.default = "derived"

    return base, derived


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
    base, derived = declare()

    # check the defaults
    inventory = base._pyre_Inventory
    assert inventory.common.value == "base - common"
        
    inventory = derived._pyre_Inventory
    assert inventory.extra.value == "derived - extra"
    assert inventory.common.value == "derived - common"
        
    # make the components available
    return base, derived


# main
if __name__ == "__main__":
    test()


# end of file 
