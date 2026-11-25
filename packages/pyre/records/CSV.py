# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


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
        Build immutable record instances from a csv formatted source
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
        Read the values of the measures of {layout}, a subclass of {pyre.records.Record}, from a
        csv formatted source, one tuple per row

        If {uri} is given, it is opened for reading in the manner recommended by the {csv}
        package, and closed when the rows run out or the caller stops reading; otherwise the
        rows come from {stream}, which is left open for its owner. The first row holds the
        headers that name the columns.
        """
        # a {uri} names a file that is ours to open
        if uri is not None:
            # so open it, and close it when the reading is done
            with open(uri, newline="") as stream:
                # pull the values from it
                yield from self.parse(layout=layout, stream=stream, **kwds)
            # and stop
            return
        # without a stream to read from
        if stream is None:
            # there is nothing to read
            raise self.SourceSpecificationError()
        # otherwise, pull the values from the stream
        yield from self.parse(layout=layout, stream=stream, **kwds)
        # all done
        return

    def parse(self, layout, stream, **kwds):
        """
        Read the values of the measures of {layout} from the csv formatted {stream}, one tuple
        per row, after a first row of headers that name the columns
        """
        # access the package
        import csv

        # build a reader
        reader = csv.reader(stream, **kwds)
        # get the headers
        headers = next(reader)
        # find the column of each measure of the layout, if the source has one
        columns = tuple(layout.pyre_selectColumns(headers=headers))
        # pair each measure with its column
        sources = tuple(zip(layout.pyre_measures, columns))
        # start reading lines from the input source
        for row in reader:
            # assemble a value for each measure, from its column or its default, and yield them
            yield tuple(
                measure.default if column is None else row[column] for measure, column in sources
            )
        # all done
        return

    def write(self, sheet, uri=None, stream=None, **kwds):
        """
        Write the records of {sheet} to a csv formatted destination

        The argument {sheet} is a {pyre.tabular} sheet: its fields name the columns, and each of
        its records fills a row, after a first row of headers.

        If {stream} is given, the rows are written to it, and it is left open for its owner;
        otherwise {uri} is opened for writing in the manner recommended by the {csv} package, and
        closed once the rows are written, and it defaults to the name of the sheet with a {.csv}
        extension
        """
        # a {stream} belongs to the caller
        if stream is not None:
            # so write the rows to it, and leave it open
            self.save(sheet=sheet, stream=stream, **kwds)
            # and stop
            return
        # without a {uri}
        if uri is None:
            # form one from the name of the sheet
            uri = sheet.pyre_name + ".csv"
        # open the file, which is ours to close
        with open(uri, "w", newline="") as stream:
            # and write the rows to it
            self.save(sheet=sheet, stream=stream, **kwds)
        # all done
        return

    def save(self, sheet, stream, **kwds):
        """
        Write the records of {sheet} to the csv formatted {stream}, after a first row of headers
        that name the columns
        """
        # access the package
        import csv

        # build a writer
        writer = csv.writer(stream, **kwds)
        # save the headers
        writer.writerow(field.name for field in sheet.pyre_fields)
        # go through the data
        for record in sheet:
            # write each one
            writer.writerow(record)

        # all done
        return

    # exceptions
    from .exceptions import SourceSpecificationError


# end of file
