# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# access to the pyre package
import pyre
# my ancestors
from .LineMill import LineMill
from .Expression import Expression


# my declaration
class Python(LineMill, Expression):
    """
    Support for python
    """


    # traits
    version = pyre.properties.str(default='')
    version.doc = "the version of python to use on the hash-bang line"

    languageMarker = pyre.properties.str(default='Python')
    languageMarker.doc = "the language marker"

    script = pyre.properties.bool(default=False)
    script.doc = "controls whether to render a hash-bang line appropriate for script files"


    # interface
    @pyre.provides
    def render(self, document):
        """
        Layout the {document} using my stationery for the header and footer
        """
        # render the hash-bang line
        if self.script:
            yield "#!/usr/bin/env python" + self.version
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
