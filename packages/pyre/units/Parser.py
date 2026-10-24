# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


from ..patterns.Singleton import Singleton

# the evaluator of text
from ..calc.evaluation import evaluate

# the report of a name that is not a unit
from .exceptions import UnknownUnitError


class Parser(metaclass=Singleton):
    """
    Singleton that converts string representations of dimensional quantities into instances of
    Dimensional
    """

    # interface
    def parse(self, text, context=None):
        """
        Convert the string representation in {text} into a dimensional quantity
        """
        # check for "none"
        if text.strip().lower() == "none":
            # do as told
            return None

        # if the caller did not supply a context
        if context is None:
            # use ours
            context = self.context
        # otherwise
        else:
            # create a new one
            context = context.copy()
            # and merge mine in it
            context.update(self.context)

        # attempt to
        try:
            # evaluate the expression, with access to the builtins a setting may use
            quantity = evaluate(expression=text, context=context)
        # if it uses a name that is in none of my piles, it is most likely a misspelled unit
        except NameError as error:
            # so say which one
            raise UnknownUnitError(name=error.name) from error
        # if all goes well, return the {quantity}
        return quantity

    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)
        self.context = self._initializeContext()
        return

    # implementation details
    def _initializeContext(self):
        """
        Build the initial list of resolvable unit symbols
        """
        # get the list of default packages
        from . import quantities

        # initialize the pile
        context = {}
        # go through all the supported quantities
        for quantity in quantities():
            # extract the symbols and their value
            for symbol, value in quantity.__dict__.items():
                # skip symbols that are in the reserved python namespace
                if not symbol.startswith("__"):
                    # add the rest to the pile
                    context[symbol] = value
        # and return it
        return context

    # access to the dimensional factory
    from . import dimensional


# end of file
