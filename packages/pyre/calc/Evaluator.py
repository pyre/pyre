# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import weakref
from . import _metaclass_Evaluator


class Evaluator(metaclass=_metaclass_Evaluator):
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
        self._owner = weakref.proxy(owner)
        return self


    def finalize(self):
        """
        Shut down
        """
        self._owner = None
        return


    # private data
    _owner = None


# end of file 
