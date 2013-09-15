# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2013 all rights reserved
#


class BlockComments:
    """
    The block based commenting strategy
    """


    # implemented interface
    def commentBlock(self, lines):
        """
        Create a comment block out of the given {lines}
        """
        # build the leader
        leader = self.leader + self.commentMarker
        # place the start comment block marker
        yield self.leader + self.startBlock
        # iterate over the {lines}
        for line in lines:
            yield leader + ' ' + line
        # place the end comment block marker
        yield self.leader + ' ' + self.endBlock

        # all done
        return


    def commentLine(self, line):
        """
        Mark {line} as a comment
        """
        # if the line is non-empty
        if line:
            # mark it
            return self.leader + self.startBlock + ' ' + line + ' ' + self.endBlock
        # otherwise, just return the comment characters
        return line


    # meta methods
    def __init__(self, startBlock, commentMarker, endBlock, **kwds):
        super().__init__(**kwds)
        self.endBlock = endBlock
        self.startBlock = startBlock
        self.commentMarker = commentMarker
        return


# end of file 
