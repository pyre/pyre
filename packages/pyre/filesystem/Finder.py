# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


import re
from .Explorer import Explorer


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
        if pattern:
            pattern = re.compile(pattern)

        # now traverse the contents and build the pathnames
        for node, trace in self._explore(node=folder, path=[]):
            # build the path out of the trace
            path = self.PATH_SEPARATOR.join(trace)
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
        # traverse its contents
        for name, child in node.contents.items():
            # add the name of this child to the path trace
            path.append(name)
            # build the string
            yield (child, path)
            # recurse into its children
            for node, path in self._explore(node=child, path=path):
                yield (node, path)
            # remove it from the trace
            path.pop()

        return


    # constants
    from . import PATH_SEPARATOR


# end of file 
