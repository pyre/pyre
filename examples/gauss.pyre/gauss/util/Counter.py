# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


class Counter(object):
    """
    A stream filter that merely counts the number of objects that have passed through it
    """


    # public data
    count = 0


    # meta methods
    def __init__(self, start=0, **kwds):
        super().__init__(**kwds)
        self.count = start
        return


    def __call__(self, stream):
        """
        Count the number of objects in {stream} and pass them through
        """
        # loop through the iterable
        for item in stream:
            # update the count
            self.count += 1
            # pass the entry through
            yield item
        # all done
        return


# end of file 
