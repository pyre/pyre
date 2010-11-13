# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
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
    precomputing data slices.

    See {pyre.tabular.Pivot} and the {pyre.tabular.Dimension} subclasses for more details.
    """


    # types
    pyre_Sheet = None # the class of fact sheets this chart is designed to analyze


    # public data
    # class data
    pyre_dimensions = () # the tuple of aggregation dimensions
    pyre_localDimensions = () # the tuple of aggregation dimensions declared locally in this Chart
    pyre_inheritedDimensions = () # the tuple of aggregation dimensions inherited from superclasses
    # instance data
    pyre_facts = None # the associated fact sheet
    pyre_bins = None # local storage for the dimension bins


    # interface
    def project(self, facts):
        # iterate over all facts
        for rank, fact in enumerate(facts):
            # and over al my dimensions
            for dimension in self.pyre_dimensions:
                # ask each one to bin this fact
                self.pyre_bins[dimension].project(record=fact, rank=rank)

        return


    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)
        # initialize the bin storage
        bins = {}
        # iterate over my dimensions
        for dimension in self.pyre_dimensions:
            # ask for the bin handler and deposit it in my local storage
            bins[dimension] = dimension.pyre_register(chart=self)
        # attach the bin storage
        self.pyre_bins = bins
        
        return

        # iterate over all the records
        for index, record in enumerate(facts):
            print("{}: {}".format(index, record))

        return


# end of file 
