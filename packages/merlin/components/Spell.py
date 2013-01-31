# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# externals
import itertools
# access the framework
import pyre


# declaration
class Spell(pyre.protocol, family="merlin.spells"):
    """
    Protocol declaration for merlin spells
    """


    # types
    from pyre.schema import uri

    # public data
    merlin = None # gets patched during boot


    # interface
    @pyre.provides
    def main(self, **kwds):
        """
        This is the action of the spell
        """


    @pyre.provides
    def help(self, **kwds):
        """
        Generate the help screen associated with this spell
        """


    # support for framework requests
    @classmethod
    def pyre_find(cls, uri, symbol, **kwds):
        """
        Participate in the search for the spell {symbol}
        """
        # access the merlin executive
        merlin = cls.merlin
        # and its private file space
        vfs = merlin.vfs

        # starting with the locations on the search paths
        roots = tuple(folder.address for folder in merlin.searchpath)
        # the locations of spells
        spells = [ 'spells' ]
        # inject the address of the {uri}
        address = [ uri.address ]
        # the leaves
        leaves = [ '{}.py'.format(symbol), '']

        # with all possible combinations of all these
        for fragments in itertools.product(roots, spells, address, leaves):
            # assemble the  path
            path = vfs.join(*filter(None, fragments))
            # build a uri and yield it
            yield cls.uri(scheme='vfs', address=path)

        # out of ideas
        return
        

# end of file 
