# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# externals
import journal
import merlin


# declaration
class Info(merlin.shells.command, family='merlin.cli.info'):
    """
    Display helpful information about various aspects of the application
    """


    @merlin.export(tip="display information about the host")
    def host(self, plexus, **kwds):
        """
        Display information about the host
        """
        # get the host
        host = self.pyre_host

        # make a channel
        channel = journal.info("merlin.info.host")
        # report
        channel.line(f"          name: {host.hostname}")
        channel.line(f"      nickname: {host.nickname}")
        channel.line(f"            os: {host.platform} {host.release} ({host.codename})")
        channel.line(f"          arch: {host.cpus.architecture}")
        channel.line(f"         cores: {host.cpus.cores}")
        # flush
        channel.log()

        # all done
        return


    @merlin.export(tip="display information about the platform")
    def platform(self, plexus, **kwds):
        """
        Display information about the platform
        """
        # get the host
        host = self.pyre_host

        # unpack
        platform = host.platform
        release = host.release
        codename = host.codename
        arch = host.cpus.architecture
        tag = f"{host.tag}"

        # make a channel
        channel = journal.info("merlin.info.platform")
        # report
        channel.line(f"            os: {platform} {release} ({codename})")
        channel.line(f"          arch: {arch}")
        channel.line(f"           tag: {tag}")
        # flush
        channel.log()

        # all done
        return


    @merlin.export(tip="display information about the user")
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

        # get the list of projects
        projects = ", ".join(project.pyre_name for project in plexus.projects)

        # make a channel
        channel = journal.info("merlin.info.workspace")
        # report
        channel.line(f"     workspace: {ws}")
        channel.line(f"        config: {cfg}")
        channel.line(f"      projects: {projects}")
        # flush
        channel.log()

        # all done
        return


# end of file
