# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# externals
import journal
import re
import subprocess

# support
import merlin


# the git source control system wrapper
class Git(
    merlin.component, family="merlin.scs.git", implements=merlin.protocols.external.scs
):
    """
    The git source control system
    """

    # setup
    name = "git"
    branchArgs = ["branch", "--show-current"]
    describeArgs = ["describe", "--tags", "--long", "--always"]
    hashArgs = ["log", "--format=format:%h", "-n", "1"]
    versionArgs = ["--version"]

    # interface
    @merlin.export
    def branch(self, driver=None):
        """
        Get the name of the currently active branch
        """
        # the git command line
        cmd = self.branchCmd(driver=driver)
        # settings
        options = {
            "executable": driver,
            "args": cmd,
            "stdout": subprocess.PIPE,
            "stderr": subprocess.PIPE,
            "universal_newlines": True,
            "shell": False,
        }
        # invoke
        with subprocess.Popen(**options) as git:
            # collect the output
            stdout, _ = git.communicate()
            # get the status
            status = git.returncode
            # if successful
            if status == 0:
                # get the branch name
                branch = stdout.strip()
                # and return it
                return branch
        # if anything went wrong, issue a warning
        channel = journal.warning("merlin.scs.git")
        # that git failed
        channel.line(f"git failed with code {status}")
        channel.line(f"while attempting to retrieve the active branch name")
        # flush
        channel.log()
        # and bail
        return "unknown"

    @merlin.export
    def hash(self, driver=None):
        """
        Get the hash of the current HEAD
        """
        # the git command line
        cmd = self.hashCmd(driver=driver)
        # settings
        options = {
            "executable": driver,
            "args": cmd,
            "stdout": subprocess.PIPE,
            "stderr": subprocess.PIPE,
            "universal_newlines": True,
            "shell": False,
        }
        # invoke
        with subprocess.Popen(**options) as git:
            # collect the output
            stdout, _ = git.communicate()
            # get the status
            status = git.returncode
            # if successful
            if status == 0:
                # get the hash
                hash = stdout.strip()
                # and return it
                return hash
        # if something went wrong, issue a warning
        channel = journal.warning("merlin.scs.git")
        # that git failed
        channel.line(f"git failed with code {status}")
        channel.line(f"while attempting to retrieve the hash of HEAD")
        # flush
        channel.log()
        # and bail
        return "unknown"

    @merlin.export
    def revision(self, driver=None):
        """
        Extract workspace revision meta-data from a git repository
        """
        # the git command line
        cmd = self.describeCmd(driver=driver)
        # the value to return on failure
        bail = (0, 0, 0, "")
        # settings
        options = {
            "executable": driver,
            "args": cmd,
            "stdout": subprocess.PIPE,
            "stderr": subprocess.PIPE,
            "universal_newlines": True,
            "shell": False,
        }
        # invoke
        with subprocess.Popen(**options) as git:
            # collect the output
            stdout, stderr = git.communicate()
            # get the status
            status = git.returncode
            # if something went wrong
            if status != 0:
                # issue a warning
                channel = journal.warning("merlin.scs.git")
                # that git failed
                channel.line(f"git failed with code {status}")
                channel.line(f"while attempting to retrieve the active branch name")
                # flush
                channel.log()
                # bail
                return bail
            # get the description
            description = stdout.strip()
            # parse it
            match = self._descriptionParser.match(description)
            # if everything went ok
            if match:
                # extract the version info
                major = match.group("major") or bail[0]
                minor = match.group("minor") or bail[1]
                micro = match.group("micro") or bail[2]
                commit = match.group("commit") or bail[3]
                # and return it
                return (int(major), int(minor), int(micro), commit)

        # if something went wrong, it is most likely a bug
        channel = journal.firewall("merlin.scs.git")
        # complain
        channel.line(f"git returned '{description}'")
        channel.line(f"which the parser couldn't understand")
        channel.line(f"while looking for the repository revision")
        # flush
        channel.log()
        # and, just in case firewalls aren't fatal, bail
        return bail

    @merlin.export
    def version(self, driver=None, **kwds):
        """
        Extract the version of git
        """
        # get the command line
        cmd = self.versionCmd(driver=driver)
        # set up the shell command
        settings = {
            "executable": driver,
            "args": cmd,
            "stdout": subprocess.PIPE,
            "stderr": subprocess.PIPE,
            "universal_newlines": True,
            "shell": False,
        }
        # make a pipe
        with subprocess.Popen(**settings) as pipe:
            # get the text source
            stream = pipe.stdout
            # and the recognizer
            regex = self._versionParser
            # the first line is the version
            line = next(stream).strip()
            # extract the fields
            match = regex.match(line)
            # if we got a match
            if match:
                # extract the version fields
                major = match.group("major")
                minor = match.group("minor")
                micro = match.group("micro")
                # assemble the version tuple and return it
                return major, minor, micro
        # otherwise, report failure with the correct structure
        return "unknown", "unknown", "unknown"

    # framework hooks
    # builder specific behavior
    def make(self, builder, driver=None, **kwds):
        """
        Generate a makefile fragment that extracts repository revision information into
        the canonical variable names
        """
        # get the describe command
        cmd = " ".join(self.describeCmd(driver=driver))
        # get the renderer
        renderer = builder.renderer

        # repository info
        yield renderer.commentLine(f"get the repository revision information")
        # record it
        yield from renderer.set(name="ws.tag", value=f"$(shell cd $(ws) && {cmd})")
        # convert into a space delimited list
        yield renderer.commentLine(f"get the repository revision information")
        # record it
        yield from renderer.set(name="ws.words", value=f"$(subst -, ,$(ws.tag))")
        # extract the tag
        yield renderer.commentLine(f"extract the version tag")
        # record it
        yield from renderer.set(
            name="ws.version",
            value=f"$(subst ., ,$(patsubst v%,%,$(word 1,$(ws.words))))",
        )
        # and the revision
        yield renderer.commentLine(f"extract the commit SHA")
        # record it
        yield from renderer.set(
            name="ws.revision", value=f"$(patsubst g%,%,$(word 3,$(ws.words)))"
        )
        # get the major version
        yield renderer.commentLine(f"extract the major version")
        # record it
        yield from renderer.set(name="ws.major", value=f"$(word 1,$(ws.version))")
        # get the minor version
        yield renderer.commentLine(f"extract the minor version")
        # record it
        yield from renderer.set(name="ws.minor", value=f"$(word 2,$(ws.version))")
        # get the micro version
        yield renderer.commentLine(f"extract the micro version")
        # record it
        yield from renderer.set(name="ws.micro", value=f"$(word 3,$(ws.version))")
        # make some room
        yield ""
        # all done
        return

    # command line generation
    def branchCmd(self, driver=None):
        """
        Build the command line that extracts repository revision information
        """
        # first the driver
        yield self.driverCmd(driver=driver)
        # and now the rest of the command line
        yield from self.branchArgs
        # all done
        return

    def describeCmd(self, driver=None):
        """
        Build the command line that extracts repository revision information
        """
        # first the driver
        yield self.driverCmd(driver=driver)
        # and now the rest of the command line
        yield from self.describeArgs
        # all done
        return

    def hashCmd(self, driver=None):
        """
        Build the command line that extracts repository revision information
        """
        # first the driver
        yield self.driverCmd(driver=driver)
        # and now the rest of the command line
        yield from self.hashArgs
        # all done
        return

    def versionCmd(self, driver=None):
        """
        Build the command line that extracts repository revision information
        """
        # first the driver
        yield self.driverCmd(driver=driver)
        # and now the rest of the command line
        yield from self.versionArgs
        # all done
        return

    def driverCmd(self, driver=None):
        """
        Generate the reference to my executable to use as the driver
        """
        # sort out the driver
        driver = driver if driver is not None else self.name
        # and return it
        return driver

    # private data
    # parser of the {git describe} result
    _descriptionParser = re.compile(
        r"(v(?P<major>\d+)\.(?P<minor>\d+).(?P<micro>\d+)-\d+-g)?(?P<commit>.+)"
    )
    # parser of the tool version
    _versionParser = re.compile(
        "".join(
            [
                r"(?P<tag>.+)\s+version\s+",
                r"(?P<major>\d+)\.(?P<minor>\d+)\.(?P<micro>\d+)",
            ]
        )
    )


# end of file
