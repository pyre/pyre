# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


import merlin


def test():
    
    class spell(merlin.spell, family="merlin.spells.test"):
        """
        A sample spell
        """
        @merlin.export
        def main(self):
            return "{.pyre_name}: main".format(self)
    
    return spell


# end of file 
