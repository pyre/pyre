# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from ..config.Slot import Slot as Base


class Slot(Base):
    """
    A specialization of {pyre.config.Slot} for storing the traits of components

    This slot enhances the calculation of the slot's value by running it through the casting
    and validation procedures specified by the associated trait
    """


    # meta methods
    def __init__(self, descriptor, **kwds):
        super().__init__(**kwds)
        self._descriptor = descriptor
   

    # private data
    _descriptor = None


# end of file 
