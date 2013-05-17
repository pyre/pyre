# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


class Processor:
    """
    The base class for decorators that attach value processors to record fields
    """


    # public data
    fields = () # the sequence of record fields that i decorate


    # meta methods
    def __init__(self, fields=fields, **kwds):
        # chain up
        super().__init__(**kwds)
        # record which fields i decorate
        self.fields = tuple(fields)
        # all done
        return


    def __call__(self, method):
        raise NotImplementedError(
            "class {.__name__!r} must implement '__call__'".format(type(self)))


# end of file 
