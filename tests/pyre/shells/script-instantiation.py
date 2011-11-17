#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Instantiate a script
"""


def test():
    
    # access to the package
    import pyre

    # declare a trivial application
    class application(pyre.application):
        """a sample application"""

        @pyre.export
        def main(self): return 0

    # build a script
    script = pyre.script(name="test")#, application=application)

    #
    return


# main
if __name__ == "__main__":
    test()


# end of file 
