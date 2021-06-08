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
        host = plexus.pyre_host

        # make a channel
        channel = journal.info("merlin.info.host")
        # report
        channel.line(f"         name: {host.hostname}")
        channel.line(f"     nickname: {host.nickname}")
        channel.line(f"           os: {host.platform} {host.release} ({host.codename})")
        channel.line(f"         arch: {host.cpus.architecture}")
        channel.line(f"        cores: {host.cpus.cores}")
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
        user = plexus.pyre_user

        # make a channel
        channel = journal.info("merlin.info.user")
        # report
        channel.line(f"     username: {user.username} ({user.uid})")
        channel.line(f"         home: {user.home}")
        channel.line(f"         name: {user.name}")
        channel.line(f"        email: {user.email}")
        channel.line(f"  affiliation: {user.affiliation}")
        # flush
        channel.log()

        # all done
        return


# end of file
