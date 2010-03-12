# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import weakref
from . import _metaclass_Evaluator


class Evaluator(object, metaclass=_metaclass_Evaluator):
    """
    Base class for the objects that are responsible for computing the value of nodes
    """


    # interface
    def validate(self, span, clean):
        """
        Check for faults
        """
        return


    def compute(self):
        """
        Compute my value
        """
        raise NotImplementedError(
            "class {0.__class__.__name__!r} must override 'compute'".format(self))


    # life cycle management
    def initialize(self, owner):
        """
        Prepare to start computing
        """
        # print("Evaluator@0x{0:x}.initialize: owner=Node@0x{1:x}".format(id(self), id(owner)))
        self._owner = weakref.proxy(owner)
        return self


    def finalize(self):
        """
        Shut down
        """
        self._owner = None
        return


    # meta methods
    # uncomment them for debugging
    # def __init__(self, **kwds):
        # super().__init__(**kwds)
        # print("Evaluator@0x{0:x}.__init__".format(id(self)))
        # return
              

    # def __del__(self, **kwds):
        # print("Evaluator@0x{0:x}.__del__".format(id(self)))
        # return


    # private data
    _onwer = None


# end of file 
