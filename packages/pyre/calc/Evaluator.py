# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


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
        return self


    def finalize(self, owner):
        """
        Shut down
        """
        return


# end of file 
