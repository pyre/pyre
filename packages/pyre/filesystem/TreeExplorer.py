# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .SimpleExplorer import SimpleExplorer

class TreeExplorer(SimpleExplorer):
    """
    A visitors that creates an tree representation of the name and node type of the contenst of
    a filesystem
    """


    def onFolder(self, folder, name, **kwds):
        """
        Handler for generic folders
        """
        # print out the directory`
        self._render(name=name, node=folder, code="d")

        # get the directory contents
        nodes = list(folder.contents.items())
        # if the directory is empty, return
        if not nodes:
            return

        # update the indentation level
        self._indent += 1

        # save graphics
        filler = self._filler
        graphic = self._graphic

        # update them
        self._filler = filler + " | "
        self._graphic = filler + " +-"

        # do all but the last one
        for name, entry in nodes[:-1]:
            entry.identify(self, name=name)
        name, entry = nodes[-1]
        # because it has special graphics
        self._graphic = filler + " `-"
        self._filler = filler + "   "
        entry.identify(self, name=name)

        # restore graphics
        self._filler = filler
        self._graphic = graphic

        return



    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)
        self._filler = ''
        self._graphic = ''
        return


    # implementation details
    def _render(self, name, node, code):
        self.printout.append(
            "{0} {2} ({1})".format(self._graphic, code, name)
            )
        return


# end of file 
