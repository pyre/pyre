# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
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


    # constants
    from . import separator


    # interface
    def explore(self, folder, pattern=None):
        """
        Traverse the folder and print out its contents
        """
        # build the regular expression
        if pattern: pattern = re.compile(pattern)

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
    def _explore(self, node, path):
        """
        The recursive workhorse for folder exploration
        """
        # first, return the current node and its path
        yield (node, path)
        # if {node} is not a folder, we are done
        if not node.isFolder: return
        # otherwise, traverse its contents
        for name, child in node.contents.items():
            # add the name of this child to the path trace
            path.append(name)
            # explore it
            for node, path in self._explore(node=child, path=path): yield (node, path)
            # remove the name of the child from the trace
            path.pop()

        return


# end of file 
