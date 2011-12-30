# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


import merlin


class test(merlin.spell, family="merlin.spells.test"):
    """
    A sample spell
    """
    @merlin.export
    def main(self):
        return "{.pyre_name}: main".format(self)


# end of file 
