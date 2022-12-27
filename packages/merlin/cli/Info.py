# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# externals
import journal
import merlin


# declaration
class Info(merlin.shells.command, family='merlin.cli.info'):
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

        # set up a marker
        indent = " " * 2
        # make a channel
        channel = journal.info("merlin.builder")
        # show me
        channel.line(f"builder:")
        channel.line(f"{indent*1}abi: {builder.abi(plexus=plexus)}")
        channel.line(f"{indent*1}type: {', '.join(builder.type)}")
        channel.line(f"{indent*1}tag: {builder.tag}")
        channel.line(f"{indent*1}/stage:")
        channel.line(f"{indent*2}seed: {builder.stage}")
        channel.line(f"{indent*2}mounted at: {vfs['/stage'].uri}")
        channel.line(f"{indent*1}/prefix:")
        channel.line(f"{indent*2}seed: {builder.prefix}")
        channel.line(f"{indent*2}abi tagged: {builder.tagged}")
        channel.line(f"{indent*2}mounted at: {vfs['/prefix'].uri}")
        channel.line(f"{indent*1}/prefix layout:")
        channel.line(f"{indent*2}bin: {prefix.bin}")
        channel.line(f"{indent*2}lib: {prefix.lib}")
        channel.line(f"{indent*2}include: {prefix.include}")
        channel.line(f"{indent*2}doc: {prefix.doc}")
        channel.line(f"{indent*2}share: {prefix.share}")
        channel.line(f"{indent*2}etc: {prefix.etc}")
        channel.line(f"{indent*2}config: {prefix.config}")
        channel.line(f"{indent*2}var: {prefix.var}")
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
        # indentation
        indent = " " * 2
        # get the list of compilers
        compilers = plexus.compilers

        # if there are any
        if compilers:
            # sign on
            channel.line(f"{indent*0}compilers:")

        # go through them
        for compiler in compilers:
            # report
            channel.line(f"{indent*1}{compiler}")
            channel.line(f"{indent*2}driver: {compiler.driver}")
            channel.line(f"{indent*2}version: {'.'.join(compiler.version())}")
        # flush
        channel.log()

        # all done
        return


    @merlin.export(tip="display host information")
    def host(self, plexus, **kwds):
        """
        Display information about the host
        """
        # indentation
        indent = " " * 2
        # get the host
        host = self.pyre_host

        # make a channel
        channel = journal.info("merlin.info.host")
        # report
        channel.line(f"{indent*0}name: {host.hostname}")
        channel.line(f"{indent*0}nickname: {host.nickname}")
        channel.line(f"{indent*0}os: {host.distribution} {host.release} ({host.codename})")
        channel.line(f"{indent*0}arch: {host.cpus.architecture}")
        channel.line(f"{indent*0}cores: {host.cpus.cores}")
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
        language = merlin.protocols.language
        # assemble its implementors
        languages = tuple(
            name for _, name, _ in language.pyre_locateAllImplementers(namespace="merlin")
        )

        # marker
        indent = " " * 2

        # make a channel
        channel = journal.info("merlin.info.host")
        # report
        channel.line(f"{indent*0}languages:")
        for name in languages:
            channel.line(f"{indent*1}{name}")
        # flush
        channel.log()

        # all done
        return


    @merlin.export(tip="display platform information")
    def platform(self, plexus, **kwds):
        """
        Display information about the platform
        """
        # indentation
        indent = " " * 2
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
        channel.line(f"{indent*0}os: {distribution} {release} ({codename})")
        channel.line(f"{indent*0}arch: {arch}")
        channel.line(f"{indent*0}tag: {tag}")
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
        channel.line(f"          user: {user.username} ({user.uid})")
        channel.line(f"          home: {user.home}")
        channel.line(f"          name: {user.name}")
        channel.line(f"         email: {user.email}")
        channel.line(f"   affiliation: {user.affiliation}")
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

        # marker
        indent = " " * 2

        # make a channel
        channel = journal.info("merlin.info.workspace")
        # report
        channel.line(f"workspace: {ws}")
        channel.line(f"config: {cfg}")

        # get the list of projects
        projects = plexus.projects
        # if there are any
        if projects:
            # start a new section
            channel.line(f"projects:")
            # go through them
            for project in projects:
                # show the name
                channel.line(f"{indent*1}{project.pyre_name}")
                # get its libraries
                libraries = project.libraries
                # if there are any
                if libraries:
                    # display
                    channel.line(f"{indent*2}libraries:")
                    # go through them
                    for library in libraries:
                        # display the name
                        channel.line(f"{indent*3}{library.pyre_name}")
                        # the stem
                        channel.line(f"{indent*4}name: {library.name}")
                        # the path relative to the repository root
                        channel.line(f"{indent*4}root: {library.root}")
                        # get the source languages
                        languages = ", ".join(language.name for language in library.languages)
                        # display their names
                        channel.line(f"{indent*4}languages: {languages}")
        # flush
        channel.log()

        # all done
        return


# end of file
