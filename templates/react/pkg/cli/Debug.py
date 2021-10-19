# -*- coding: utf-8 -*-
#
# {project.authors}
# (c) {project.span} all rights reserved


# externals
import journal
# support
import {project.name}


# declaration
class Debug({project.name}.shells.command, family='{project.name}.cli.debug'):
    """
    Display debugging information about this application
    """


    # user configurable state
    root = {project.name}.properties.str()
    root.default = None
    root.tip = "specify the portion of the namespace to display"

    full = {project.name}.properties.bool()
    full.default = False
    full.tip = "control whether to do a full dive"


    @{project.name}.export(tip="dump the application configuration namespace")
    def config(self, plexus, **kwds):
        """
        Generate a list of encountered configuration files
        """
        # make a channel
        channel = journal.info("{project.name}.cli.config")
        # set up the indentation level
        indent = " " * 2

        # get the configurator
        cfg = self.pyre_configurator
        # go through its list of sources
        for uri, priority in cfg.sources:
            # tell me
            channel.line(f"{{indent}}{{uri}}, priority '{{priority.name}}'")

        # flush
        channel.log()

        # all done
        return 0


    @{project.name}.export(tip="dump the application configuration namespace")
    def nfs(self, plexus, **kwds):
        """
        Dump the application configuration namespace
        """
        # make a channel
        channel = journal.info("{project.name}.cli.nfs")
        # set up the indentation level
        indent = " " * 2

        # get the prefix
        prefix = "{project.name}" if self.root is None else self.root
        # and the name server
        nameserver = self.pyre_nameserver

        # get all nodes that match my {{prefix}}
        for info, node in nameserver.find(pattern=prefix):
            # attempt to
            try:
                # get the node value
                value = node.value
            # if anything goes wrong
            except nameserver.NodeError as error:
                # use the error message as the value
                value = f" ** ERROR: {{error}}"
            # inject
            channel.line(f"{{indent}}{{info.name}}: {{value}}")

        # flush
        channel.log()

        # all done
        return 0


    @{project.name}.export(tip="dump the application configuration namespace")
    def vfs(self, plexus, **kwds):
        """
        Dump the application virtual filesystem
        """
        # get the prefix as a path
        prefix = {project.name}.primitives.path(
            "/{project.name}" if self.root is None else self.root)

        # starting at the root of the {{vfs}}
        folder = plexus.vfs
        # go through the {{prefix}} intermediate folder carefully
        for part in prefix.parts:
            # try to
            try:
                # look up the folder
                folder = folder[part]
            # if anything goes wrong
            except folder.NotFoundError:
                # make a channel
                channel = journal.error("merlin.debug.vfs")
                # complain
                channel.line(f"could not find '{{part}}' in '{{folder.uri}}'")
                channel.line(f"while scanning for '{{prefix}}' in the virtual file system")
                # flush
                channel.log()
                # and bail if errors aren't fatal
                return 1
            # if the folder exists, get its contents
            folder.discover(levels=1)

        # if the user wants to see everything
        if self.full:
            # dive
            folder.discover()

        # build the report
        report = folder.dump(indent=1)

        # make a channel
        channel = journal.info("{project.name}.cli.vfs")
        # sign in
        channel.line(f"vfs: prefix='{{prefix}}'")
        # dump
        channel.report(report=report)
        # flush
        channel.log()

        # all done
        return 0


# end of file
