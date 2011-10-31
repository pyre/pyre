# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# declaration
class Selection:
    """
    Encapsulation of the results of a {select} query
    """


    # public data
    query = None # the query that generated the selection
    results = None # the result set from the query


    # meta methods
    def __init__(self, query, results):
        self.query = query
        self.results = results
        return


    def __iter__(self):
        """
        Wrap each result tuple as record as return it
        """
        # get the headers
        headers = next(self.results)
        # iterate over the result set
        for result in self.results:
            # build and instance of the query embedded record type
            record = self.query.pyre_Record(raw=result)
            # return it to the caller
            yield record
        # all done
        return


    def __len__(self):
        """
        Compute and return the number of records selected by the {query}
        """
        return len(self.results)


# end of file 
