# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


import pyre
from ..components import spell


class Spell(pyre.component, implements=spell):
    """
    Interface declaration for merlin spells
    """


    # public state
    dry = pyre.properties.bool(default=False)
    dry.doc = 'show what would be done without actually doing anything'


    # access to the merlin executive
    merlin = None # patched by the merlin boot sequence


    @property
    def vfs(self):
        """
        Access to my file server
        """
        return self.merlin.vfs


    # interface
    @pyre.export
    def main(self, *args, **kwds):
        """
        This is the action of the spell
        """
        print(" ** casting {!r}".format(self.pyre_name))
        # all done
        return


    @pyre.export
    def help(self, **kwds):
        """
        Generate the help screen associated with this spell
        """
        # by default, dump my docstring
        for line in self.__doc__: print(line.strip())
        # all done
        return


    def __init__(self, name, **kwds):
        super().__init__(name=name, **kwds)

        # prepare the journal
        # access the package
        import journal
        # build the channels
        self.info = journal.info(name)
        self.warning = journal.warning(name)
        self.error = journal.error(name)

        # all done
        return


# end of file 
