# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# externals
import re
# my superclass
from .Explorer import Explorer


# class declaration
class Finder(Explorer):
    """
    A visitor that generates a list of the contents of a filesystem
    """


    # interface
    def explore(self, folder, pattern='.*'):
        """
        Traverse the folder and return contents that match the given pattern
        """
        # build the regular expression
        pattern = re.compile(pattern)

        # now traverse the contents
        for node in self._explore(node=folder):
            # compare the node {uri} against the pattern
            match =  pattern.match(str(node.uri))
            # and if the path matches
            if match:
                # return the pair
                yield node, match

        # all done
        return


    # implementation details
    def _explore(self, node):
        """
        The recursive workhorse for folder exploration
        """
        # first, return the current node and its path
        yield node
        # if {node} is not a folder, we are done
        if not node.isFolder: return
        # otherwise, traverse its contents
        for child in node.contents.values():
            # explore it
            yield from self._explore(node=child)
        # all done
        return


# end of file
