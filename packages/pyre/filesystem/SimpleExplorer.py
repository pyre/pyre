# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# my superclass
from .Explorer import Explorer


# class declaration
class SimpleExplorer(Explorer):
    """
    A visitor that creates an indented list of the name and node type of the contents of a
    filesystem
    """

    # interface
    def explore(self, node, label):
        """
        Traverse the filesystem and print out its contents
        """
        # build a representation of the current node
        yield self.render(name=label, node=node)

        # if {node} is not a directory, we are done
        if not node.isFolder:
            return

        # otherwise, increase the indentation level
        self._indent += 1
        # iterate over the folder contents
        for name, child in sorted(node.contents.items()):
            # generate the content report
            for description in self.explore(node=child, label=name):
                yield description
        # decrease the indentation level back
        self._indent -= 1

        # all done
        return

    # meta methods
    def __init__(self, indent=0, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the starting indentation level
        self._indent = indent
        # all done
        return

    # implementation details
    def render(self, name, node):
        # compute the indent
        indent = self.INDENT * self._indent
        # build a string and return it
        return f"{indent}({node.marker}) {name}"

    # constants
    INDENT = " " * 2


# end of file
