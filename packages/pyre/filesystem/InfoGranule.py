# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from .InfoFile import InfoFile


# declaration
class InfoGranule(InfoFile):
    """
    The metadata of a filesystem entry that stands for a granule found by a search of a data
    catalog: the record the catalog returned, and the parts of it every client wants at hand
    """

    # metamethods
    def __init__(self, record, size, links, begin, end, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the catalog record in its entirety, for clients that want to dig
        self.record = record
        # the total size of the granule payload, in bytes
        self.size = size
        # the links to the granule payload, by the scheme of the route that reaches it, e.g. the
        # {https} ones through the data center and the {s3} ones straight to its storage
        self.links = links
        # the start of the acquisition
        self.begin = begin
        # and its end
        self.end = end
        # all done
        return


# end of file
