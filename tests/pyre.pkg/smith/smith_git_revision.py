#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that smith places the project it assembles under source control: a repository with
the initial revision, tagged 'v0.0.1'
"""

# support
import journal
import pyre
import pyre.smith


def test():
    """
    Generate a project and check that its initial revision is recorded and tagged
    """
    # for the scratch area, and for asking git about the result
    import os
    import subprocess
    import tempfile

    # give git an identity, so the initial revision can be recorded wherever the test runs
    os.environ.update(
        GIT_AUTHOR_NAME="pyre tests",
        GIT_AUTHOR_EMAIL="tests@pyre.invalid",
        GIT_COMMITTER_NAME="pyre tests",
        GIT_COMMITTER_EMAIL="tests@pyre.invalid",
    )

    # work in a scratch area
    with tempfile.TemporaryDirectory() as scratch:
        # go there
        os.chdir(scratch)
        # make the app, with a project that spells everything the templates ask for
        app = pyre.smith.smith(name="smith_git_revision")
        app.project = "basic"
        app.project.name = "hello"
        app.project.authors = "the authors"
        app.project.span = "2026"
        app.project.github = "authors/hello"
        # silence the progress report, since what matters is the outcome
        journal.info("smith").deactivate()
        # generate the project
        status = app.run()
        # it went well
        assert status == 0
        # ask git for the tagged revision
        tag = subprocess.run(
            ["git", "rev-parse", "--verify", "--quiet", "v0.0.1^{commit}"],
            cwd="hello",
            capture_output=True,
            text=True,
        )
        # it is there
        assert tag.returncode == 0
        # ask git whether anything was left out of it
        status = subprocess.run(
            ["git", "status", "--porcelain"], cwd="hello", capture_output=True, text=True
        )
        # nothing was
        assert status.returncode == 0 and status.stdout == ""
    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
