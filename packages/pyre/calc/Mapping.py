# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# class declaration
class Mapping:
    """
    Mix-in class that forms the basis of the representation of mappings
    """


    # types
    from .exceptions import CircularReferenceError


    # public data
    @property
    def operands(self):
        """
        Iterate over my operands
        """
        # easy enough
        yield from self.data.values()


    # interface
    def getValue(self, **kwds):
        """
        Compute and return my value
        """
        # return the value of each operand
        return {name: op.value for name, op in self.data.items()}


    # meta-methods
    def __init__(self, operands, **kwds):
        # chain up
        super().__init__(**kwds)
        # my operands are in a dict
        self.data = dict(**operands)
        # all done
        return


    # implementation details
    def _substitute(self, current, replacement):
        """
        Adjust the operands by substituting {replacement} for {current} in the list of operands
        at position {index}
        """
        # go through my data
        for name, operand in self.data.items():
            # if we found the match
            if operand is current:
                # replace it
                self.data[name] = replacement

        # all done
        return self


# end of file
