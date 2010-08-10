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

    # try to instantiate one and catch the exception
    # NYI: 
    #     this should be a journal.firewall eventually
    #     catch the ImportError for now, until journal gets implemented, at which point this
    #     test will start to fail and it will need fixing
    try:
        interface()
        assert False
    except ImportError:
        pass
     
    return interface


# main
if __name__ == "__main__":
    test()


# end of file 
