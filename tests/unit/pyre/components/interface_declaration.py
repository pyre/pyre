#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Declare a non-trivial interface
"""


def test():
    # access
    import pyre.components
    from pyre.components.Interface import Interface
    from pyre.components.Property import Property

    # declare an interface
    class interface(Interface):
        """a trivial interface"""
        # traits
        a = Property()
        b = Property()
        # interface
        @pyre.components.provides
        def behavior(self):
            """a method required of all compatible implementations"""

    # check that everything is as expected
    assert interface._pyre_configurables == (interface, Interface)
    # look through the namemap
    namemap = interface._pyre_Inventory._pyre_namemap
    assert namemap["a"] == "a"
    assert namemap["b"] == "b"
    # access the trait categories
    categories = interface._pyre_Inventory._pyre_categories
    assert len(categories) == 2
    # assert categories["behaviors"] == (interface.behavior,)
    assert categories["properties"] == (interface.a, interface.b)

    # verify that the interface is not instantiatable
    try:
        interface()
        assert False
    except Exception:
        pass
     
    return interface


# main
if __name__ == "__main__":
    test()


# end of file 
