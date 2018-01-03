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

    @pyre.export
    def main(self, *args, **kwds):
        """
        The main entry point
        """
        # get my terminal
        term = self.pyre_executive.terminal
        # putting things back to normal
        normal = term.colors['normal']
        # loop
        for r in range(6):
            for g in range(6):
                for b in range(6):
                    # splice
                    code = "{}{}{}".format(r,g,b)
                    # get the color sequence
                    color = term.rgb256(code, foreground=False)
                    # say hello
                    print("{}  {}".format(color, normal), end='')
                print(end=' ')
            print()

        # all done
        return


# main
if __name__ == "__main__":
    # build one
    app = ColorTable('colors')
    # runt it
    status = app.run()
    # and pass the result on
    raise SystemExit(status)


# end of file
