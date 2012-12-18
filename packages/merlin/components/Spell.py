# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
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
    def pyre_find(cls, uri, symbol):
        """
        Participate  in the search for shelves consistent with {uri}
        """
        # get the merlin executive
        merlin = cls.merlin
        # and its private namespace
        vfs = merlin.vfs
        # visit each location on the merlin search path
        for root in merlin.searchpath:
            # form the location of the subdirectory with spells
            spelldir = vfs.join(root.address, 'spells')
            # get the folder
            folder = vfs[spelldir]

            # if the uri has an address
            if uri.address:
                # just look for it
                candidates = [ uri.address ]
            # otherwise
            else:
                # visit all the files
                candidates = list(
                    name for name, node in folder.contents.items() if not node.isFolder)
            
            # for each target
            for candidate in candidates:
                # build a {uri} for it
                uri = cls.uri(scheme='vfs', address=vfs.join(spelldir, candidate))
                # and send it to the caller
                yield uri
        # all done
        return


    @classmethod
    def pyre_find(cls, uri, symbol):
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

        # all ideas exhausted
        return
        


# end of file 
