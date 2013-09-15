# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2013 all rights reserved
#


class CSV:
    """
    A reader and writer of records in csv format

    This class enhances the support provided by the csv package from the python standard
    library by reading and writing records that have a variety of metadata attached to their
    fields, which enables much smarter processing of the information content.
    """


    # record factories
    def immutable(self, layout, uri=None, stream=None, **kwds):
        """
        Build mutable record instances from a csv formatted source
        """
        # for each record in the input stream
        for data in self.read(layout=layout, uri=uri, stream=stream, **kwds):
            # get the immutable record constructor to do its thing
            yield layout.pyre_immutable(data=data)
        # all done
        return


    def mutable(self, layout, uri=None, stream=None, **kwds):
        """
        Build mutable record instances from a csv formatted source
        """
        # for each record in the input stream
        for data in self.read(layout=layout, uri=uri, stream=stream, **kwds):
            # get the mutable record constructor to do its thing
            yield layout.pyre_mutable(data=data)
        # all done
        return


    # support
    def read(self, layout, uri=None, stream=None, **kwds):
        """
        Read lines from a csv formatted input source

        The argument {layout} is expected to be a subclass of {pyre.records.Record}. It will be
        inspected to extract the names of the columns to ingest.

        If {uri} is not None, it will be opened for reading in the manner recommended by the
        {csv} package; if {stream} is given instead, it will be passed directly to the {csv}
        package. The first record is assumed to be headers that name the columns of the data.
        """
        # check whether {uri} was provided
        if uri:
            # build the associated stream
            stream = open(uri, newline='')
        # look for a valid stream
        if not stream:
            raise self.SourceSpecificationError()
        # access the package
        import csv
        # build a reader
        reader = csv.reader(stream, **kwds)
        # get the headers
        headers = next(reader)
        # build the name map
        index = { name: offset for offset, name in enumerate(headers) }
        # adjust the column specification
        columns = tuple(layout.pyre_selectColumns(headers=index))
        # start reading lines from the input source
        for row in reader:
            # assemble the requested data tuple and yield it
            yield (row[column] for column in columns)
        # all done
        return


    # exceptions
    from .exceptions import SourceSpecificationError


# end of file 
