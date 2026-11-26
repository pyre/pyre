# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import journal
import os
import pyre
import shlex
import shutil
import subprocess

# my protocol
from ...Cluster import Cluster as protocol


# declaration
class Cluster(pyre.component, family="pyre.db.clusters.postgres", implements=protocol):
    """
    A postgres cluster: the data directory of a server, and the server that runs on it

    The cluster is made by {initdb} and its server is started and stopped by {pg_ctl}, which
    run as programs of their own, so managing a cluster needs no connection to it
    """

    # user configurable state
    # where the server programs live
    programs = pyre.properties.path()
    programs.default = None
    programs.doc = "the directory with the server programs; unset, they are found on the PATH"

    # where the cluster lives
    data = pyre.properties.path()
    data.default = None
    data.doc = "the data directory of the cluster"

    # where its server listens for local clients
    socket = pyre.properties.path()
    socket.default = None
    socket.doc = "the directory of the unix socket of the server; unset, the data directory"

    # the port of the server
    port = pyre.properties.int()
    port.default = 5432
    port.doc = "the port the server listens on, which also names its unix socket"

    # who owns the cluster
    user = pyre.properties.str()
    user.default = None
    user.doc = "the superuser of the cluster; unset, the user that makes it"

    # how clients prove who they are
    authentication = pyre.properties.str()
    authentication.default = "trust"
    authentication.doc = "how the server authenticates its clients"

    # how the databases store text
    encoding = pyre.properties.str()
    encoding.default = "UTF8"
    encoding.doc = "the encoding of the databases of the cluster"

    # how they sort it and spell their messages
    locale = pyre.properties.str()
    locale.default = None
    locale.doc = "the locale of the databases of the cluster; unset, the one of the environment"

    # where the server listens for clients on the network
    addresses = pyre.properties.strings()
    addresses.default = []
    addresses.doc = "the network addresses the server listens on; empty, its unix socket only"

    # whether the cluster must survive a crash
    durable = pyre.properties.bool()
    durable.default = True
    durable.doc = "whether the server makes sure that what it writes reaches the disk"

    # where the server writes its log
    log = pyre.properties.path()
    log.default = None
    log.doc = "the log file of the server; unset, the data directory with the suffix '.log'"

    # interface
    @pyre.export
    def init(self):
        """
        Make the cluster, unless it exists already
        """
        # a cluster needs a place to live
        if not self.placed():
            # and there is none
            return self
        # if there is a cluster in my data directory
        if self.initialized():
            # there is nothing to do
            return self
        # find the program that makes clusters
        initdb = self.program(name="initdb")
        # if it is not there
        if initdb is None:
            # the cluster cannot be made
            return self
        # assemble the settings of the new cluster
        arguments = [
            "--pgdata",
            self.data,
            "--encoding",
            self.encoding,
            "--auth",
            self.authentication,
        ]
        # if there is a superuser to name
        if self.user is not None:
            # name it
            arguments += ["--username", self.user]
        # if there is a locale to set
        if self.locale is not None:
            # set it
            arguments += ["--locale", self.locale]
        # a cluster that need not survive a crash
        if not self.durable:
            # can skip waiting for its files to reach the disk
            arguments += ["--no-sync"]
        # make it
        self.execute(program=initdb, arguments=arguments)
        # all done
        return self

    @pyre.export
    def start(self):
        """
        Start the server of the cluster, and wait until it accepts connections
        """
        # a cluster needs a place to live
        if not self.placed():
            # and there is none
            return self
        # if the server is running
        if self.status():
            # there is nothing to do
            return self
        # a server needs a cluster to run on
        if not self.initialized():
            # so complain
            channel = journal.error("pyre.db.cluster")
            # about its absence
            channel.log(f"there is no postgres cluster in '{self.data}'")
            # and bail
            return self
        # find the program that runs servers
        pgctl = self.program(name="pg_ctl")
        # if it is not there
        if pgctl is None:
            # the server cannot be started
            return self
        # make the directory of the socket
        self.sockets().mkdir(parents=True, exist_ok=True, mode=0o700)
        # the server listens on its socket, and on the addresses it is given
        options = [
            "-k",
            str(self.sockets()),
            "-p",
            str(self.port),
            "-c",
            f"listen_addresses={','.join(self.addresses)}",
        ]
        # a server that need not survive a crash
        if not self.durable:
            # can skip waiting for its writes to reach the disk
            options += ["-c", "fsync=off"]
        # start the server, and wait until it is ready; {pg_ctl} hands the options to a shell
        self.execute(
            program=pgctl,
            arguments=["start", "--pgdata", self.data, "--log", self.logfile(), "--wait"]
            + ["--options", shlex.join(options)],
        )
        # all done
        return self

    @pyre.export
    def stop(self):
        """
        Stop the server of the cluster
        """
        # a cluster needs a place to live
        if not self.placed():
            # and there is none
            return self
        # if the server is not running
        if not self.status():
            # there is nothing to do
            return self
        # find the program that runs servers
        pgctl = self.program(name="pg_ctl")
        # stop the server, ending the sessions that are open, and wait until it is gone
        self.execute(
            program=pgctl, arguments=["stop", "--pgdata", self.data, "--mode", "fast", "--wait"]
        )
        # all done
        return self

    @pyre.export
    def status(self):
        """
        Check whether the server of the cluster is running
        """
        # a server needs a cluster to run on
        if not self.placed() or not self.initialized():
            # so there is none
            return False
        # find the program that runs servers
        pgctl = self.program(name="pg_ctl")
        # if it is not there
        if pgctl is None:
            # there is no way to tell
            return False
        # ask it whether the server is running
        outcome = subprocess.run(
            [pgctl, "status", "--pgdata", self.data],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        # it answers with its exit status
        return outcome.returncode == 0

    @pyre.export
    def remove(self):
        """
        Stop the server of the cluster, and delete the cluster
        """
        # a cluster needs a place to live
        if not self.placed():
            # and there is none
            return self
        # stop the server
        self.stop()
        # if it is still running, its cluster is still in use
        if self.status():
            # so leave it alone
            return self
        # if the data directory is there
        if self.data.exists():
            # it must hold a cluster, or it is not mine to delete
            if not self.initialized():
                # so complain
                channel = journal.error("pyre.db.cluster")
                # say what is wrong
                channel.log(f"'{self.data}' does not hold a postgres cluster")
                # and leave it alone
                return self
            # delete the cluster
            shutil.rmtree(self.data)
        # if the socket lives in a directory of its own
        if self.socket is not None:
            # clear it
            self.clearSockets()
        # all done
        return self

    @pyre.export
    def restart(self):
        """
        Replace whatever cluster is there with a fresh one, and start its server
        """
        # a cluster needs a place to live
        if not self.placed():
            # and there is none
            return self
        # remove the cluster, make a new one, and start its server
        return self.remove().init().start()

    # implementation details
    def placed(self):
        """
        Check whether i was given a data directory
        """
        # if i was
        if self.data is not None:
            # all is well
            return True
        # otherwise, complain
        channel = journal.error("pyre.db.cluster")
        # about the missing setting
        channel.log("the postgres cluster has no data directory")
        # and let the caller decide what to do
        return False

    def initialized(self):
        """
        Check whether my data directory holds a cluster
        """
        # a cluster records the version of the server that made it
        return (self.data / "PG_VERSION").exists()

    def sockets(self):
        """
        The directory of the socket of the server
        """
        # the one i was given, or the data directory
        return self.socket if self.socket is not None else self.data

    def logfile(self):
        """
        The log file of the server
        """
        # if i was given one
        if self.log is not None:
            # use it
            return self.log
        # otherwise, it sits beside the data directory, named after it
        return self.data.parent / f"{self.data.name}.log"

    def clearSockets(self):
        """
        Remove the directory of the socket of my server, along with what my server left in it
        """
        # if the directory is not there
        if not self.socket.exists():
            # there is nothing to do
            return self
        # a server that did not shut down cleanly leaves its socket and its lock behind
        for name in [f".s.PGSQL.{self.port}", f".s.PGSQL.{self.port}.lock"]:
            # form the path
            leftover = self.socket / name
            # and if it is there
            if leftover.exists():
                # remove it
                os.unlink(leftover)
        # the directory itself goes only if nothing else lives in it
        try:
            # remove it
            os.rmdir(self.socket)
        # if something else lives in it
        except OSError:
            # leave it in place
            channel = journal.warning("pyre.db.cluster")
            # and say so
            channel.log(f"the socket directory '{self.socket}' is not empty, so it was kept")
        # all done
        return self

    def program(self, name):
        """
        Find the server program {name}
        """
        # if i was told where the server programs live
        if self.programs is not None:
            # form the path to this one
            candidate = self.programs / name
            # if it is there
            if candidate.isFile():
                # hand it over
                return candidate
            # otherwise, describe where it was looked for
            where = f"in '{self.programs}'"
        # otherwise
        else:
            # look for it on the PATH
            candidate = shutil.which(name)
            # if it is there
            if candidate is not None:
                # hand it over
                return pyre.primitives.path(candidate)
            # otherwise, describe where it was looked for
            where = "on the PATH"
        # complain
        channel = journal.error("pyre.db.cluster")
        # about the missing program
        channel.log(f"could not find the postgres program '{name}' {where}")
        # and let the caller decide what to do
        return None

    def execute(self, program, arguments):
        """
        Run {program} with {arguments}, and report its output when it fails
        """
        # run the program, collecting what it says
        outcome = subprocess.run(
            [program, *arguments],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        # if it worked
        if outcome.returncode == 0:
            # it has nothing to say that matters
            return True
        # otherwise, make a channel
        channel = journal.error("pyre.db.cluster")
        # name what failed
        channel.line(f"'{program.name} {arguments[0]}' failed with status {outcome.returncode}")
        # set what it said apart
        channel.indent()
        # show it
        channel.report(outcome.stdout.splitlines())
        # and return to the margin
        channel.outdent()
        # and flush
        channel.log()
        # let the caller know
        return False


# end of file
