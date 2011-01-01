# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


class Dimension:
    """
    The base class for implementing data binning strategies
    """


    # public data
    measure = None # the sheet descriptor that i am responsible for binning
    offset = None # the field offset with a sheet record that contains the data i bin


    # interface
    def pyre_register(self, chart):
        """
        Build a bin handler for a newly built {chart}
        """
        raise NotImplementedError(
            "class {.__class__.__name__!r} must implement 'pyre_register'".format(self))


    # meta methods
    def __init__(self, measure, **kwds):
        super().__init__(**kwds)
        self.measure = measure
        return


    def __get__(self, instance, cls):
        """
        Implementation of the descriptor read interface
        """
        try:
            return instance.pyre_bins[self]
        except AttributeError:
            return self

        import journal
        firewall = journal.firewall("pyre.tabular")
        return firewall.log(
            "{.__class__.__name__!r}: chart {} is not initialized properly".format(self, instance))


# end of file 
