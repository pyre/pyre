# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


class Printer(object):
    """
    A stream filter that prints the objects that pass through it
    """


    # meta methods
    def __call__(self, stream):
        """
        Print the objects in the {stream} as the pass through
        """
        # loop through the iterable
        for item in stream:
            # print the item
            print(item)
            # pass it through
            yield item
        # all done
        return


# end of file 
