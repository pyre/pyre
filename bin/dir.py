#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#


# externals
import os
import re
import subprocess
# support
import pyre


# the app
class Dir(pyre.application):
    """
    A generator of colorized directory listings that is repository aware
    """


    # get color support
    from pyre.shells.CSI import CSI


    # user configurable state
    across = pyre.properties.bool(default=False)
    across.doc = "sort multi-column output across the window"

    # protocol obligations
    @pyre.export
    def main(self, *args, **kwds):
        """
        The main entry point
        """
        # build the list of directories
        directories = list(self.argv) or ['.']
        # figure out how many there are
        args = len(directories)

        # go through each on
        for directory in directories:
            # if there is more than one
            if args > 1:
                # show the one being dumped
                print(f"{directory}:")
            # get the listing and print it
            print("\n".join(self.render(directory=directory)))
            # if necessary
            if args > 1:
                # print a separator
                print()

        # all done
        return 0


    # implementation details
    def render(self, directory):
        """
        Generate the directory listing
        """
        # get the terminal
        terminal = self.executive.terminal
        # get the directory contents
        entries = self.entries(directory=directory)

        # figure out the width of the terminal
        width = terminal.width
        # deduce the layout
        layout = (1,0) if self.across else (0,1)
        # make a tabulator
        tabulator = Table(width=width, layout=layout, entries=entries)
        # get the grid
        grid = tabulator.grid
        # unpack its shape
        rows, columns = grid.tile.shape
        # ask for the column width
        columnWidth = tabulator.width

        # get the reset code from the terminal
        reset = terminal.ansi["normal"]

        # go through the rows
        for row in range(rows):
            # initialize the pile
            fragments = []
            # go through the columns
            for col in range(columns):
                # get the entry
                entry = grid[(row, col)]
                # render it
                fragments.append(entry.render(reset=reset))
                # every column other than the last
                if col < columns-1:
                    # adds a bit of padding
                    fragments.append(" "*(columnWidth - (len(entry.name)+len(entry.marker))))
            # put it all together
            yield "".join(fragments)

        # all done
        return


    def entries(self, directory):
        """
        Initialize the directory listing
        """

        # deduce the filesystem
        fs = pyre.filesystem.local(root=directory)
        # expand the top level only
        fs.discover(levels=1)

        # get the names and info nodes of the contents of the current working directory
        for name in sorted(fs.contents.keys()):
            # get the associated node
            node = fs[name]
            # and the associated meta-data
            info = fs.info(node=node)
            # make an entry
            entry = Entry()
            # set the name
            entry.name = name
            # decorate based on the file type
            info.identify(explorer=self, entry=entry)
            # publish it
            yield entry

        # all done
        return


    def gitHome(self):
        """
        Locate the root of the git worktree
        """
        # set up the command
        cmd = [ "git", "rev-parse", "--show-toplevel" ]
        # settings
        options = {
            "executable": "git",
            "args": cmd,
            "stdout": subprocess.PIPE,
            "stderr": subprocess.PIPE,
            "universal_newlines": True,
            "shell": False }
        # invoke
        with subprocess.Popen(**options) as git:
            # collect the output
            stdout, stderr = git.communicate()
            # if there was no error
            if git.returncode == 0:
                # read the location of the repository root
                root = stdout.strip()
                # and return it
                return root
        # all done
        return None


    # callbacks for identifying file types
    def onBlockDevice(self, entry, info):
        """
        Decorate block devices
        """
        # mark it
        entry.marker = '\u2584'
        # all done
        return entry


    def onCharacterDevice(self, entry, info):
        """
        Decorate character devices
        """
        # mark it
        entry.marker = "#"
        # all done
        return entry


    def onFile(self, entry, info):
        """
        Decorate regular files
        """
        # if the user has execute permissions
        if info.mode(entity=info.user, access=info.execute):
            # mark it
            entry.marker = "*"
        # all done
        return entry


    def onFolder(self, entry, info):
        """
        Decorate folders
        """
        # mark it
        entry.marker = "/"
        # all done
        return entry


    def onLink(self, entry, info):
        """
        Decorate symbolic links
        """
        # mark it
        entry.marker = '@' #"\u2192"

        # if the link is broken
        if info.referent is None:
            # colorize the marker
            entry.markerColor = self.CSI.csi24(red=0xc0, green=0x20, blue=0x20)
        # all done
        return entry


    def onNamedPipe(self, entry, info):
        """
        Decorate named pipes
        """
        # mark it
        entry.marker = "|"
        # all done
        return entry


    def onSocket(self, entry, info):
        """
        Decorate sockets
        """
        # mark it
        entry.marker = "="
        # all done
        return entry


# helpers
class Entry:
    """
    The information necessary for rendering a directory entry
    """


    # public data
    name = ""
    marker = ""
    nameColor = ""
    markerColor = ""


    # interface
    def render(self, reset):
        """
        Render me
        """
        # collect the fragments
        label = [
            self.nameColor, self.name, reset,
            self.markerColor, self.marker, reset
        ]
        # assemble
        return "".join(label)


class Table:
    """
    The builder of the listing layout
    """


    # public data
    grid = None


    # meta-methods
    def __init__(self, entries, width, layout=None, **kwds):
        # chain up
        super().__init__(**kwds)
        # make the grid, which adjust my shape and width as a side effect
        self.grid = self.makeGrid(maxWidth=width, layout=layout, entries=entries)
        # all done
        return


    # implementation details
    def makeGrid(self, maxWidth, entries, layout):
        """
        Make a grid out of the directory {entries}
        """
        # realize the container
        data = tuple(self.tabulate(maxWidth=maxWidth, entries=entries))
        # which deduces the table shape as a side effect
        shape = self.shape
        # get the grid factory
        import pyre.grid
        # make one
        grid = pyre.grid.grid(shape=shape, layout=layout, data=data)
        # and return it
        return grid


    def tabulate(self, maxWidth, entries):
        """
        Generate the entry container and its shape
        """
        # initialize the stats
        longestName = 0
        longestMarker = 0
        numEntries = 0

        # go through the entries
        for entry in entries:
            # update the size
            numEntries += 1
            # update the longest name
            longestName = max(longestName, len(entry.name))
            # and the longest marker
            longestMarker = max(longestMarker, len(entry.marker))
            # publish
            yield entry

        # if there were no entries
        if numEntries == 0:
            # make a trivial shape
            self.shape = (0,0)
            # and bail
            return

        # compute the minimum width of a column, accounting for my file type marker and a margin
        minWidth = longestName + longestMarker + 2
        # the grid width
        columns = max(min(maxWidth // minWidth, numEntries), 1)
        # and the grid height
        lines = numEntries // columns + (1 if numEntries % columns else 0)

        # record the minimum required column width
        self.width = minWidth
        # set the shape
        self.shape = (lines, columns)

        # pad
        for _ in range(lines*columns - numEntries):
            # with blank entries
            yield Entry()

        # all done
        return


    # private data
    width = 0
    shape = None


# bootstrap
if __name__ == "__main__":
    # instantiate
    app = Dir(name="dir")
    # invoke
    status = app.run()
    # share
    raise SystemExit(status)


# end of file
