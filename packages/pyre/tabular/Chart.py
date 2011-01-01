# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Aggregator import Aggregator


class Chart(metaclass=Aggregator):
    """
    The base class for imposing coördinate systems on sheets

    A chart contains the specification of a number of dimensions that enable the categorization
    and analysis of the facts in a sheet. For example, given a sales table that contains
    transaction information that includes date, sku and amount, a chart with these three
    dimensions would simplify answering questions such as "compute the total sales of a given
    sku in a given time period".

    Charts are used by pivot tables as a means of imposing structure on the data and
    precomputing data slices. Charts ar enot useful by themslevs since they cannot be used to
    directly reference the facts in a sheet; they only provide access through record ranks, and
    independent access to the fact sheet is record before actual records can be retrieved.

    See {pyre.tabular.Pivot} and the {pyre.tabular.Dimension} subclasses for more details.
    """


    # types
    pyre_Sheet = None # the class of fact sheets this chart is designed to analyze


    # public data
    # class data
    pyre_dimensions = () # the tuple of aggregation dimensions
    pyre_namemap = None

    pyre_localDimensions = () # the tuple of aggregation dimensions declared locally in this Chart
    pyre_inheritedDimensions = () # the tuple of aggregation dimensions inherited from superclasses
    # instance data
    pyre_bins = None # local storage for the dimension bins


    # interface
    def pyre_initialize(self):
        """
        Make a chart ready to process records from a sheet by initializing its bin strategies
        """
        # check whether we've already done this
        if self._pyre_initialized: return self
        # otherwise, iterate over my dimensions
        for dimension in self.pyre_dimensions:
            # and initialize my bin handlers
            self.pyre_bins[dimension].initialize()
        # set the flag
        self._pyre_initialized = True
        # and return
        return self


    def pyre_project(self, facts):
        """
        Iterate through {facts} and bin each one accroding to the user specified dimensions
        """
        # make sure i have been initialized
        self.pyre_initialize()
        # iterate over all facts
        # make sure this happens in one pass through the data, in case the source is a stream
        for rank, fact in enumerate(facts):
            # and over al my dimensions
            for dimension in self.pyre_dimensions:
                # ask each one to bin this fact
                self.pyre_bins[dimension].project(record=fact, rank=rank)
        # all done
        return


    def pyre_filter(self, **kwds):
        """
        Create an iterable over those facts that statisfy the criteria specified in {kwds},
        which is assumed to be a value specification for each dimension that is to be used to
        restrict the data set
        """
        # identify the relevant bins
        bins = (self.pyre_namemap[name][value] for name, value in kwds.items())
        # build and return the restriction
        return set.intersection(*bins)


    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)
        # initialize the bin storage
        bins = {}
        namemap = {}
        # iterate over my dimensions
        for dimension in self.pyre_dimensions:
            # build the bin handler
            handler = dimension.pyre_register(chart=self)
            # attach it to the bin registry
            bins[dimension] = handler
            # and the name map
            namemap[dimension.name] = handler
        # attach the bin storage
        self.pyre_bins = bins
        # and the namemap
        self.pyre_namemap = namemap
        # all done
        return


    # private data
    _pyre_initialized = False


# end of file 
