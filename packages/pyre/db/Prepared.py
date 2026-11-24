# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# declaration
class Prepared:
    """
    A statement rendered once, whose slots take their values each time it runs

    The statement is written by {build} into a place for its values that the mill of my {server}
    makes, which keeps the constants the statement holds and the slots it leaves open. My server
    decides how the statement reaches the back end when it runs, and where it keeps it there, in
    {name} and {session}. With a {selection}, a run hands back the rows the statement produces,
    as records of the selection: one at a time when {stream} is set, as {select} does, and all at
    once otherwise
    """

    # interface
    def run(self, **values):
        """
        Run the statement, with its slots filled in from {values}
        """
        # fill in the slots, refusing a slot without a value, and a value without a slot
        arguments = self.parameters.bind(values=values)
        # let my server run the statement
        rows = self.server._runPrepared(prepared=self, values=values, arguments=arguments)
        # a statement that hands back no rows
        if self.selection is None:
            # hands back nothing
            return None
        # the others hand back their rows, as records of the selection
        records = self.server._records(rows=rows, selection=self.selection)
        # one at a time, or all at once
        return records if self.stream else list(records)

    def close(self):
        """
        Release whatever my server keeps on the back end on my behalf
        """
        # my server knows what that is
        self.server._releasePrepared(prepared=self)
        # all done
        return self

    # meta-methods
    def __init__(self, server, build, selection=None, stream=False, **kwds):
        # chain up
        super().__init__(**kwds)
        # the server that runs me
        self.server = server
        # the recipe of the statement, which writes it into a place for its values
        self.build = build
        # the records of the rows the statement hands back, if it hands any back
        self.selection = selection
        # whether the rows come back one at a time
        self.stream = stream
        # a place for the values of the statement, which keeps its constants and its slots
        self.parameters = server.sql.parameters()
        # the statement, rendered once
        self.lines = tuple(build(self.parameters))
        # where my server keeps the statement on the back end, under what name, once it does
        self.name = None
        self.session = None
        # all done
        return

    def __enter__(self):
        """
        Hand me over for the length of a block
        """
        # easy enough
        return self

    def __exit__(self, exc_type, exc_instance, exc_traceback):
        """
        Release what my server keeps on my behalf when the block ends
        """
        # release it, whether the block finished or raised
        self.close()
        # and let whatever the block raised go on
        return False


# end of file
