#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved

"""
Exercise the ability to inject an unrelated component into the configuration space of an existing
one
"""

# support
import pyre
import journal


# the reader protocol
class Reader(pyre.protocol, family="inject.readers"):
    """
    The reader specification
    """

    # required state
    dtype = pyre.properties.str()
    dtype.doc = "the data type"


# a table of flags
class Table(pyre.protocol, family="inject.tables"):
    """
    A table of flags
    """

    # state
    channel = pyre.properties.bool()
    zoom = pyre.properties.bool()
    scroll = pyre.properties.bool()
    path = pyre.properties.bool()

    @classmethod
    def pyre_default(self, **kwds):
        """
        The default implementation
        """
        return Sync


# the view protocol
class View(pyre.protocol, family="inject.views"):
    """
    The view specification
    """

    # required state
    channel = pyre.properties.str()
    channel.doc = "the name of the channel to visualize"

    sync = Table()
    sync.doc = "a collection of named flags"


# a reader implementation
class Flat(pyre.component, family="inject.readers.flat", implements=Reader):
    """
    A reader that opens flat files
    """

    # state
    dtype = pyre.properties.str()
    dtype.default = None
    dtype.doc = "the data type"


class Sync(pyre.component, family="inject.sync", implements=Table):
    """
    A table of flags
    """

    # state
    channel = pyre.properties.bool(default=False)
    zoom = pyre.properties.bool(default=False)
    scroll = pyre.properties.bool(default=False)
    path = pyre.properties.bool(default=False)


# a view implementation
class Panel(pyre.component, family="inject.views.panel", implements=View):
    """
    The configuration of a panel with a view to some data
    """

    # required state
    channel = pyre.properties.str()
    channel.default = None
    channel.doc = "the name of the channel to visualize"

    zoom = pyre.properties.int()
    zoom.default = 0
    zoom.doc = "the zoom level"

    sync = Table()
    sync.doc = "a collection of named flags"


# the app
class Inject(pyre.application, family="inject.applications"):
    """
    The app
    """

    # state
    reader = Reader()
    reader.doc = "my reader"

    # main entry point
    @pyre.export
    def main(self, *args, **kwds):
        """
        The main entry point
        """
        # get my reader
        reader = self.reader
        # and an ad hoc view that's connected to it by injecting in its configuration namespace
        view = Panel(name=f"{reader.pyre_name}.view")

        # make a channel
        channel = journal.info("inject.logging")
        # show me
        channel.line(f"reader: {reader}")
        channel.indent()
        channel.line(f"name: {reader.pyre_name}")
        channel.line(f"dtype: {reader.dtype}")
        channel.outdent()

        # comment this out, if you want to see the output
        journal.quiet()
        # show me
        channel.line(f"view: {view}")
        channel.indent()
        channel.line(f"name: {view.pyre_name}")
        channel.line(f"channel: {view.channel}")
        channel.line(f"zoom: {view.zoom}")
        channel.line(f"sync: {view.sync}")
        channel.indent()
        channel.line(f"channel: {view.sync.channel}")
        channel.line(f"zoom: {view.sync.zoom}")
        channel.line(f"scroll: {view.sync.scroll}")
        channel.line(f"path: {view.sync.path}")
        channel.outdent()
        channel.outdent()
        # flush
        channel.log()

        # run the checks against the known configuration from the yaml file
        assert reader.pyre_name == "c16"
        assert reader.dtype == "complex128"
        assert view.pyre_name == f"{reader.pyre_name}.view"
        assert view.channel == "complex"
        assert view.zoom == -1
        assert view.sync.channel == False
        assert view.sync.zoom == False
        assert view.sync.scroll == False
        assert view.sync.path == True

        # and done
        return 0


# bootstrap
if __name__ == "__main__":
    # instantiate
    app = Inject(name="inject.app")
    # invoke
    status = app.run()
    # share
    raise SystemExit(0)


# end of file
