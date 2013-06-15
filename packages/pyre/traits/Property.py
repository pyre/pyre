# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# externals
from .. import schemata # type information
# superclass
from .Slotted import Slotted


# declaration
@schemata.typed
class Property(Slotted):
    """
    The base class for traits that correspond to simple types
    """


    # mixins to be included to my type offering
    class decimal:
        """Mixin for handling decimal values"""

        # override the default expression handler
        @property
        def macro(self):
            """
            Return the default strategy for handling expressions in slot values
            """
            # build expressions
            return self.pyre_nameserver.expression


    class dimensional:
        """Mixin for handling quantities with units"""

        # override the default expression handler
        @property
        def macro(self):
            """
            Return the default strategy for handling expressions in slot values
            """
            # build expressions
            return self.pyre_nameserver.expression


    class float:
        """Mixin for handling floating point values"""

        # override the default expression handler
        @property
        def macro(self):
            """
            Return the default strategy for handling expressions in slot values
            """
            # build expressions
            return self.pyre_nameserver.expression


    class int:
        """Mixin for handling integer values"""

        # override the default expression handler
        @property
        def macro(self):
            """
            Return the default strategy for handling expressions in slot values
            """
            # build expressions
            return self.pyre_nameserver.expression


    # meta-methods
    def __str__(self):
        return "{0.__name!r}: a property of type {0.typename!r}".format(self)


# end of file 
