# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# superclass
from .Processor import Processor


# declaration
class Validator(Processor):
    """
    A record method decorator that registers this method as a validator of field values
    """


    # meta-methods
    def __call__(self, method):
        """
        Add {method} as a validator the my registered fields
        """
        # go through the sequence of registered fields
        for field in self.fields:
            # and register {method} as a validator
            field.validators.append(method)
        # all done
        return method
    

# end of file 
