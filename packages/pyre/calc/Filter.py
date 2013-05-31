# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#



# class declaration
class Filter:
    """
    A mix-in class that changes the values of nodes iff they pass its constraints
    """


    # interface
    def setValue(self, value, **kwds):
        """
        Override the value setter to refresh my cache and notify my observers
        """
        # go through all my constraints
        for constraint in self.constraints:
            # if any fail, leave the value unmodified
            if not constraint(value=value, node=self): return self

        # if they all succeed, update the value
        return super().setValue(value=value, **kwds)


    # meta-methods
    def __init__(self, constraints=None, **kwds):
        # chain up
        super().__init__(**kwds)
        # initialize my constraints
        self.constraints = [] if constraints is None else constraints
        # all done
        return


# end of file 
