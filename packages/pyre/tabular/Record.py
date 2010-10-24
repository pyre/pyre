# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


class Record(tuple):
    """
    The base class of sheet entries
    """


    @classmethod
    def csv_read(cls, filename=None, stream=None, columns=None, **kwds):
        """
        Read lines from a csv formatted input source

        If {filename} is not None, it will be opened for reading in the manner recommended by
        the {csv} package; if {stream} is given instead, it will be passed directly to the
        {csv} package. The first record is assumed to be headers that name the columns of the
        data.

        The optional argument {namemap} provides a mapping between the headers in the input
        source and the order in which the data is stored in the record
        """
        # check whether {filename} was provided
        if filename:
            # build the associated stream
            stream = open(filename, newline='')
        # look for a valid stream
        if not stream:
            raise SourceSpecificationError()
        # access the package
        import csv
        # build a reader
        reader = csv.reader(stream, **kwds)
        # get the headers
        headers = next(reader)
        # build the name map
        namemap = { name: index for index, name in enumerate(headers) }
        # adjust the column specification
        if columns is None:
            columns = headers
        # start reading lines from the input source
        for row in reader:
            # assemble the requested data tuple
            data = tuple( row[namemap[column]] for column in columns )
            # build record out of it
            record = cls(data)
            # and yield it
            yield record
        # all done
        return


    # exceptions
    from .exceptions import SourceSpecificationError
                


        



        


# end of file 
