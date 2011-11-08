# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Shell import Shell


class Script(Shell):
    """
    A shell that invokes the main application behavior and then exits
    """
    

    # interface
    def execute(self, *args, **kwds):
        """
        Invoke the application behavior
        """
        # NYI! delegate, for now
        return super().execute(*args, **kwds)


# end of file 
