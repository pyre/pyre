# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# externals
import journal
import merlin


# declaration
class Info(merlin.shells.command, family="merlin.cli.info"):
    """
    Display helpful information about various aspects of the application
    """

    @merlin.export(tip="display the builder configuration")
    def builder(self, plexus, **kwds):
        """
        Display the builder configuration
        """
        # get the builder
        builder = plexus.builder
        # the fileserver
        vfs = plexus.vfs
        # and the layout of the install area
        prefix = builder.layout

        # make a channel
        channel = journal.info("merlin.builder")
        # show me
        channel.line(f"builder: {builder}")
        channel.indent()
        channel.line(f"abi: {builder.abi(plexus=plexus)}")
        channel.line(f"/stage:")
        channel.indent()
        channel.line(f"seed: {builder.stage}")
        channel.line(f"mounted at: {vfs['/stage'].uri}")
        channel.outdent()
        channel.line(f"/prefix:")
        channel.indent()
        channel.line(f"seed: {builder.prefix}")
        channel.line(f"abi tagged: {builder.tagged}")
        channel.line(f"mounted at: {vfs['/prefix'].uri}")
        channel.line(f"layout:")
        channel.indent()
        channel.line(f"bin: {prefix.bin}")
        channel.line(f"lib: {prefix.lib}")
        channel.line(f"include: {prefix.include}")
        channel.line(f"doc: {prefix.doc}")
        channel.line(f"share: {prefix.share}")
        channel.line(f"etc: {prefix.etc}")
        channel.line(f"config: {prefix.config}")
        channel.line(f"var: {prefix.var}")
        channel.outdent(levels=3)
        # flush
        channel.log()

        # all done
        return

    @merlin.export(tip="display known compilers")
    def compilers(self, plexus, **kwds):
        """
        Display information about the chosen compilers
        """
        # make a channel
        channel = journal.info("merlin.info.host")
        # get the list of compilers
        compilers = plexus.compilers

        # if there are any
        if compilers:
            # sign on
            channel.line(f"compilers:")

        # push in
        channel.indent()
        # go through them
        for compiler in compilers:
            # report
            channel.line(f"{compiler}")
            channel.indent()
            channel.line(f"driver: {compiler.driver}")
            channel.line(f"version: {'.'.join(compiler.version())}")
            channel.outdent()
        # outdent
        channel.outdent()
        # flush
        channel.log()

        # all done
        return

    @merlin.export(tip="display the list of projects in the current workspace")
    def workspace(self, plexus, **kwds):
        """
        Display information about the platform
        """
        # get the virtual filesystems; they are guaranteed to exist, but may be trivial
        ws = plexus.vfs["/workspace"].uri
        cfg = plexus.pfs["/workspace"].uri
        # if they are trivial
        if str(ws) == "/workspace":
            # we were unable to locate the workspace root
            ws = "not found"
            cfg = "not found"
        # make a channel
        channel = journal.info("merlin.info.workspace")
        # report
        channel.line(f"workspace: {ws}")
        channel.line(f"branch: {plexus.scs.branch()}")
        channel.line(f"revision: {plexus.scs.revision()}")
        channel.line(f"config: {cfg}")
        # get the list of projects
        projects = plexus.projects
        # if there are any
        if projects:
            # start a new section
            channel.line(f"projects:")
            # indent
            channel.indent()
            # go through them
            for project in projects:
                # show the name
                channel.line(f"{project.pyre_name}")
                # get its libraries
                libraries = project.libraries
                # if there are any
                if libraries:
                    # indent
                    channel.indent()
                    # display
                    channel.line(f"libraries:")
                    # indent
                    channel.indent()
                    # go through them
                    for library in libraries:
                        # display the name
                        channel.line(f"{library.pyre_name}")
                        # indent
                        channel.indent()
                        # the stem
                        channel.line(f"name: {library.name}")
                        # the path relative to the repository root
                        channel.line(f"root: {library.root}")
                        # outdent
                        channel.outdent()
                    # outdent
                    channel.outdent(levels=2)
            # outdent
            channel.outdent()
        # outdent
        channel.outdent()
        # flush
        channel.log("done")

        # all done
        return

    @merlin.export(tip="display information about external packages")
    def externals(self, plexus, argv, **kwds):
        """
        Display information about external packages
        """
        # make a channel
        channel = journal.info("merlin.info.externals")
        # report
        channel.line(f"argv: {tuple(argv)}")
        channel.line(f"kwds: {kwds}")
        # flush
        channel.log()
        # all done
        return

    @merlin.export(tip="display the known source languages")
    def languages(self, plexus, **kwds):
        """
        Display information about the known source languages
        """
        # get the language protocol
        language = merlin.protocols.languages.language
        # assemble its implementors
        languages = tuple(
            name
            for _, name, _ in language.pyre_locateAllImplementers(namespace="merlin")
        )
        # make a channel
        channel = journal.info("merlin.info.host")
        # report
        channel.line(f"languages:")
        channel.indent()
        for name in languages:
            channel.line(f"{name}")
        channel.outdent()
        # flush
        channel.log()

        # all done
        return

    @merlin.export(tip="display user information")
    def user(self, plexus, **kwds):
        """
        Display information about the host
        """
        # get the host
        user = self.pyre_user

        # make a channel
        channel = journal.info("merlin.info.user")
        # report
        channel.line(f"user: {user.username} ({user.uid})")
        channel.line(f"home: {user.home}")
        channel.line(f"name: {user.name}")
        channel.line(f"email: {user.email}")
        channel.line(f"affiliation: {user.affiliation}")
        # flush
        channel.log()

        # all done
        return

    @merlin.export(tip="display host information")
    def host(self, plexus, **kwds):
        """
        Display information about the host
        """
        # get the host
        host = self.pyre_host
        # make a channel
        channel = journal.info("merlin.info.host")
        # report
        channel.line(f"name: {host.hostname}")
        channel.line(f"nickname: {host.nickname}")
        channel.line(f"os: {host.distribution} {host.release} ({host.codename})")
        channel.line(f"arch: {host.cpus.architecture}")
        channel.line(f"cores: {host.cpus.cores}")
        # flush
        channel.log()

        # all done
        return

    @merlin.export(tip="display platform information")
    def platform(self, plexus, **kwds):
        """
        Display information about the platform
        """
        # get the host
        host = self.pyre_host
        # unpack
        distribution = host.distribution
        release = host.release
        codename = host.codename
        arch = host.cpus.architecture
        tag = f"{host.tag}"
        # make a channel
        channel = journal.info("merlin.info.platform")
        # report
        channel.line(f"os: {distribution} {release} ({codename})")
        channel.line(f"arch: {arch}")
        channel.line(f"tag: {tag}")
        # flush
        channel.log()

        # all done
        return


# end of file
