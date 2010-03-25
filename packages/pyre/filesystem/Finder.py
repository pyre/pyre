# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Explorer import Explorer


class Finder(Explorer):
    """
    A visitor that generates a list of the contents of a filsystem
    """


    # interface
    def explore(self, folder, pattern=None):
        """
        Traverse the folder and print out its contents
        """
        return self._explore(node=folder, name="")
        

    # implementation details
    def _explore(self, node, name):
        """
        The recursive workhorse for folder exploration
        """
        # traverse its contents
        for childName, child in node.contents.items():
            if name:
                # return the name of this node
                path = self.PATH_SEPARATOR.join([name, childName])
                yield path
            else:
                path = childName
            for path in self._explore(node=child, name=path):
                yield path

        return


    # constants
    from . import PATH_SEPARATOR


# end of file 
