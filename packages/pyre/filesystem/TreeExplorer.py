# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# superclass
from .Explorer import Explorer


# class declaration
class TreeExplorer(Explorer):
    """
    A visitor that creates a tree representation with the name and node type of the contents of
    a folder
    """


    # interface
    def explore(self, node, label):
        """
        Traverse the filesystem and print out its contents
        """
        # build a representation of the current node
        yield self.render(name=label, node=node)

        # if {node} is not a directory, we are done
        if not node.isFolder: return

        # otherwise, grab the folder contents
        children = tuple(sorted(node.contents.items()))
        # if the folder is empty, we are done
        if not children: return

        # save the old graphics
        margin = self._margin
        graphic = self._graphic
        # update them
        self._margin = margin + ' | '
        self._graphic = margin + ' +-'
        # iterate over the folder contents, except the last one
        for name, child in children[:-1]:
            # generate the content report
            for description in self.explore(node=child, label=name): yield description
        # grab the last entry
        name, child = children[-1]
        # which gets a special graphic
        self._margin = margin + '   '
        self._graphic = margin + ' `-'
        # and explore it
        for description in self.explore(node=child, label=name): yield description
        # restore the graphics
        self._margin = margin
        self._graphic = graphic

        # all done
        return


    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)
        self._graphic = '' # the marker that goes in front of a rendered entry
        self._margin = '' # the leading string that encodes the structure of the tree
        return


    # implementation details
    def render(self, name, node):
        return "{} {} ({})".format(self._graphic, name, node.marker)


# end of file 
