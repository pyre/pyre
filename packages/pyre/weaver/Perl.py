# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# access to the pyre package
import pyre
# my ancestor
from .LineMill import LineMill


# my declaration
class Perl(LineMill):
    """
    Support for perl
    """


    # traits
    version = pyre.properties.str(default='5')
    version.doc = "the version of perl to use on the hash-bang line"


    # interface
    @pyre.provides
    def render(self, document):
        """
        Layout the {document} using my stationery for the header and footer
        """
        # render the hash-bang line
        if self.version:
            yield "#!/usr/bin/env perl" + self.version
        # and the rest
        for line in super().render(document):
            yield line
        # all done
        return


    # meta methods
    def __init__(self, **kwds):
        super().__init__(comment='#', **kwds)
        return


# end of file 
