# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# externals
import journal
import merlin


# declaration
class Libraries(merlin.shells.command, family='merlin.cli.lib'):
    """
    Access to the libraries of the current workspace
    """


    # user configurable state
    only = merlin.properties.strings()
    only.doc = "narrow the libraries to those whose name is in this set"


    # commands
    @merlin.export(tip="display the names of the selected libraries")
    def info(self, plexus, **kwds):
        """
        Display the names of the selected libraries
        """
        # marker
        indent = " " * 2
        # make a channel
        channel = journal.info("merlin.libs.names")
        # go through the set of libraries
        for lib in self.filter(projects=plexus.projects):
            # show me the asset name and its stem
            channel.line(f"{lib.pyre_name}:")
            channel.line(f"{indent*1}name: {lib.name}")
            channel.line(f"{indent*1}root: {lib.root}")
        # flush
        channel.log()
        # all done
        return


    @merlin.export(tip="display the sources of the selected libraries")
    def sources(self, plexus, **kwds):
        """
        Display the sources of the selected libraries
        """
        # ask the plexus to
        # marker
        indent = " " * 2
        # make a channel
        channel = journal.info("merlin.libs.names")

        # go through the set of libraries
        for lib in self.filter(projects=plexus.projects):
            # show me the asset name and its stem
            channel.line(f"{lib.pyre_name}:")
            channel.line(f"{indent*1}name: {lib.name}")
            channel.line(f"{indent*1}root: {lib.root}")
            channel.line(f"{indent*1} uri: {plexus.vfs['workspace'].uri / lib.root}")
            # go through the sources
            for asset in lib.assets():
                # set up a pile of markers
                markers = []
                # if the asset is marked {ignore}
                if asset.ignore:
                    # leave a marker
                    markers.append("IGNORED")
                # put them all together
                marker= ", ".join(markers)
                # assemble the line decoration
                decoration = "" if not marker else f"  ({marker})"
                # render the asset and its markers
                channel.line(f"{indent*2}{asset.pyre_name}{decoration}")

        # flush
        channel.log()
        # all done
        return


    # implementation details
    def filter(self, projects):
        """
        Build the set of libraries to access
        """
        # grab the user defined selection
        only = self.only
        # build the selector
        sieve = (lambda x: x.name in only) if only else None
        # assemble all accessible libraries
        libs = (lib for project in projects for lib in project.libraries)
        # choose
        yield from filter(sieve, libs)
        # all done
        return


# end of file