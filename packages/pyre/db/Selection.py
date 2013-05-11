# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# declaration
class Selection:
    """
    Encapsulation of the results of a {select} query
    """

    # types, so I can recognize tables and queries
    from .Query import Query
    from .Schemer import Schemer
    from .Selector import Selector


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
        # get my query object
        query = self.query
        # if it is a query class or instance
        if isinstance(query, self.Selector) or isinstance(query, self.Query):
            # delegate to my query worker
            yield from self._namedTuples()
            # all done
            return

        # if it is a table class
        if isinstance(query, self.Schemer):
            # delegate to my table worker
            yield from self._tableInstances()
            # all done
            return

        # otherwise, we have a bug; ignore, for now
        return


    def __len__(self):
        """
        Compute and return the number of records selected by the {query}
        """
        return len(self.results)


    # implementation details
    def _namedTuples(self):
        """
        Convert my results into query record instances
        """
        # cache the record type of my query object
        factory = self.query.pyre_Record
        # get the headers; ignore them, for now, since the order of the results matches exactly
        # the record order, by construction
        headers = next(self.results)

        # iterate over the result set
        for result in self.results:
            # build an instance of the query embedded record type and return it
            yield factory(raw=result)

        # all done
        return


    def _tableInstances(self):
        # cache my query object
        query = self.query
        # get the headers; ignore them, for now, since the order of the results matches exactly
        # the record order, by construction
        headers = tuple(next(self.results))

        # iterate over the result set
        for result in self.results:
            # set up the command line argument
            kwds = { name:value for name,value in zip(headers, result) }
            # build an instance of the table and return it
            yield query(**kwds)

        # all done
        return


# end of file 
