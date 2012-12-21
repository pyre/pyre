# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# externals
import re
# superclass
from .Linux import Linux


# declaration
class Ubuntu(Linux, family='pyre.platforms.ubuntu'):
    """
    Encapsulation of a host running linux on the ubuntu distribution
    """


    # public data
    release = None


    # meta-methods
    def __init__(self, **kwds):
        super().__init__(**kwds)
        self.release = self.identify()
        return


    # implementation details
    def identify(self):
        """
        Extract the revision identifier
        """
        # open the issue file
        with open(self.issue) as issue:
            # read the first line
            tag = next(issue)
            # parse
            match = re.match('Ubuntu (?P<revision>[0-9]{1,2}\.[0-9]{1,2})', tag)
            # if this fails...
            if not match: return 'unknown'
            # otherwise
            return match.group('revision')
        

# end of file 
