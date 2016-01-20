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
    def explore(self, folder, pattern=None):
        """
        Traverse the folder and print out its contents
        """
        # build the regular expression
        if pattern: pattern = re.compile(pattern)

        # now traverse the contents
        for node in self._explore(node=folder):
            # get the node uri
            path = node.uri
            # if there's no regular expression filter, or the path passes the filter
            if not pattern or pattern.match(str(path)):
                # return the pair
                yield node, path

        # all done
        return

        # now traverse the contents and build the pathnames
        for node, trace in self._explore(node=folder, path=[]):
            # build the path out of the trace
            path = self.separator.join(trace)
            # if there's no regular expression, or it matches if it's there
            if not pattern or pattern.match(path):
                # return the path
                yield node, path

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
