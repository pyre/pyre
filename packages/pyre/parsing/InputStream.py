# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# externals
import io


# declaration
class InputStream:
    """
    A wrapper over input streams that maintains location information
    """


    # meta-methods
    def __init__(self, stream, line=1, column=0, **kwds):
        # chain up
        super().__init__(**kwds)
        # if the stream is not open in text mode
        if not isinstance(stream, io.TextIOBase):
            # wrap it
            stream = io.TextIOWrapper(stream)
        # and save it
        self.stream = stream
        # all done
        return


    def __iter__(self):
        """
        When used as an iterator
        """
        # easy enough
        return enumerate(self.stream)


# end of file
