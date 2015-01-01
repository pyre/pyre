# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


from ..patterns.Singleton import Singleton


class Parser(metaclass=Singleton):
    """
    Singleton that converts string representations of dimensional quantities into instances of
    Dimensional
    """


    # interface
    def parse(self, text):
        """
        Convert the string representation in {text} into a dimensional quantity
        """
        # evaluate the expression and return the result
        return eval(text, self.context)


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
        from . import modules
        # start with an empty one
        context = {}
        # update it with the contents of all the default modules
        for module in modules():
            for symbol, value in module.__dict__.items():
                if not symbol.startswith('__'):
                    context[symbol] = value
        # and return it
        return context


    # access to the dimensional factory
    from . import dimensional


# end of file
