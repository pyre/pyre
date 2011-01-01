# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Explorer import Explorer


class SimpleExplorer(Explorer):
    """
    A visitor that creates an indented list of the name and node type of the contents of a
    filesystem
    """


    # interface
    def explore(self, filesystem):
        """
        Traverse the filesystem and print out its contents
        """
        self.printout = []
        filesystem.identify(self, name=filesystem.mountpoint)
        return self.printout


    # handlers for the various types of nodes
    def onNode(self, node, name, **kwds):
        """
        Handler for generic nodes
        """
        self._render(name=name, node=node, code='f')
        return


    def onFolder(self, folder, name, **kwds):
        """
        Handler for generic folders
        """
        self._render(name=name, node=folder, code='d')
        # up the indentation level
        self._indent += 1
        # explore the directory contents
        for name, node in folder.contents.items():
            node.identify(explorer=self, name=name)
        # decrease the indentation level
        self._indent -= 1
        # and we are done
        return


    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)
        self._indent = 0
        return


    # implementation details
    def _render(self, name, node, code):
        self.printout.append(
            "{0}({1}) {2}".format(self.INDENT*self._indent, code, name)
            )
        return


    # constants
    INDENT = ' '*2


    # private data
    printout = None


# end of file 
