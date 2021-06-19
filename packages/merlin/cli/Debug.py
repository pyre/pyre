# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# externals
import merlin


# declaration
class Debug(merlin.shells.command, family='merlin.cli.debug'):
    """
    Display debugging information about this application
    """


    # user configurable state
    prefix = merlin.properties.str()
    prefix.default = None
    prefix.tip = "specify the portion of the namespace to display"


    @merlin.export(tip="list the encountered configuration files")
    def config(self, plexus, **kwds):
        """
        Generate a list of encountered configuration files
        """
        # make a channel
        channel = plexus.info
        # set up the indentation level
        indent = " " * 2

        # get the configurator
        cfg = self.pyre_configurator
        # go through its list of sources
        for uri, priority in cfg.sources:
            # tell me
            channel.line(f"{indent}{uri}, priority '{priority.name}'")

        # flush
        channel.log()

        # all done
        return 0


    @merlin.export(tip="dump the application configuration namespace")
    def nfs(self, plexus, **kwds):
        """
        Dump the application configuration namespace
        """
        # make a channel
        channel = plexus.info
        # set up the indentation level
        indent = " " * 2

        # get the prefix
        prefix = "merlin" if self.prefix is None else self.prefix
        # and the name server
        nameserver = self.pyre_nameserver

        # get all nodes that match my {prefix}
        for info, node in nameserver.find(pattern=prefix):
            # attempt to
            try:
                # get the node value
                value = node.value
            # if anything goes wrong
            except nameserver.NodeError as error:
                # use the error message as the value
                value = f" ** ERROR: {error}"
            # inject
            channel.line(f"{indent}{info.name}: {value}")

        # flush
        channel.log()

        # all done
        return 0


    @merlin.export(tip="dump the application virtual filesystem")
    def vfs(self, plexus, **kwds):
        """
        Dump the application virtual filesystem
        """
        # make a channel
        channel = plexus.info
        # get the prefix
        prefix = '/merlin' if self.prefix is None else self.prefix
        # build the report
        report = '\n'.join(plexus.vfs[prefix].dump(indent=1))

        # sign in
        channel.line(f"vfs: prefix='{prefix}'")
        # dump
        channel.line(report)
        # flush
        channel.log()

        # all done
        return 0


# end of file
