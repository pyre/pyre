#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2018 all rights reserved
#


"""
Show me the 256 colors possible with the ANSI 256 escape sequences
"""

# support
import itertools
# framework
import pyre

# declaration
class ColorTable(pyre.application):
    """
    Build a 256 color table
    """

    # public state
    color = pyre.properties.str(default='c0c0c0')
    color.doc = 'a 6 digit hex string with the desired color value'


    # behavior
    @pyre.export
    def main(self, *args, **kwds):
        """
        The main entry point
        """
        # get my terminal
        term = self.pyre_executive.terminal
        # putting things back to normal
        normal = term.colors['normal']
        # show me
        print('{}Hello!{}'.format(term.rgb(self.color, foreground=False), normal))
        # all done
        return 0


# main
if __name__ == "__main__":
    # build one
    app = ColorTable('colors')
    # runt it
    status = app.run()
    # and pass the result on
    raise SystemExit(status)


# end of file
