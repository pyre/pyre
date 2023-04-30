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
class Git(merlin.component, family="merlin.scs.git", implements=merlin.protocols.scs):
    """
    The git source control system
    """


    # interface
    @merlin.export
    def branch(self):
        """
        Get the name of the currently active branch
        """
        # the git command line
        cmd = [ "git", "branch", "--show-current" ]
        # settings
        options = {
            "executable": "git",
            "args": cmd,
            "stdout": subprocess.PIPE,
            "stderr": subprocess.PIPE,
            "universal_newlines": True,
            "shell": False }
        # invoke
        with subprocess.Popen(**options) as git:
            # collect the output
            stdout, _ = git.communicate()
            # get the status
            status = git.returncode
            # if something went wring
            if status != 0:
                # issue a warning
                channel = journal.warning("merlin.scs.git")
                # that git failed
                channel.line(f"git failed with code {status}")
                channel.line(f"while attempting to retrieve the active branch name")
                # flush
                channel.log()
                # and bail
                return "unknown"
            # if successful, get the branch name
            branch = stdout.strip()
            # and return it
            return branch

        # if anything went wrong
        return "unknown"


    @merlin.export
    def version(self):
        """
        Extract project version meta-data from a git repository
        """
        # the value to return on failure
        bail = (0, 0, 0, "")
        # the git command line
        cmd = [ "git", "describe", "--tags", "--long", "--always" ]
        # settings
        options = {
            "executable": "git",
            "args": cmd,
            "stdout": subprocess.PIPE,
            "stderr": subprocess.PIPE,
            "universal_newlines": True,
            "shell": False }
        # invoke
        with subprocess.Popen(**options) as git:
            # collect the output
            stdout, stderr = git.communicate()
            # get the status
            status = git.returncode
            # if something went wring
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
            match = self.descriptionParser.match(description)
            # if something went wrong
            if not match:
                # this is most likely a bug
                channel = journal.firewall("merlin.scs.git")
                # complain
                channel.line(f"git returned '{description}'")
                channel.line(f"which the parser couldn't understand")
                channel.line(f"while looking for version tag")
                # flush
                channel.log()
                # and, just in case firewalls aren't fatal, bail
                return bail
            # otherwise, extract the version info
            major = match.group("major") or 1
            minor = match.group("minor") or 0
            micro = match.group("micro") or 0
            commit = match.group("commit")
            # and return it
            return (int(major), int(minor), int(micro), commit)

        # if anything else went wrong
        return bail

    # private data
    # parser of the {git describe} result
    descriptionParser = re.compile(
        r"(v(?P<major>\d+)\.(?P<minor>\d+).(?P<micro>\d+)-\d+-g)?(?P<commit>.+)"
        )


# end of file
