#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that smith reports a project it assembled but could not place under source control, quoting
git, rather than claiming success
"""

# support
import journal
import pyre
import pyre.smith


def test():
    """
    Generate a project where git has no identity, and check that the failure is reported
    """
    # for the scratch area
    import os
    import tempfile

    # the pages of the entries that reach the error channel of smith
    seen = []

    # a device that keeps the pages of the entries it receives
    class Capture(journal.device):
        """
        A device that keeps the pages of the entries it receives
        """

        def __init__(self, **kwds) -> None:
            """
            Build a device named after its purpose
            """
            # chain up
            super().__init__(name="capture", **kwds)
            # all done
            return

        def alert(self, entry: journal.entry) -> "Capture":
            """
            Keep the page of a user facing {entry}
            """
            # save the page
            seen.append(list(entry.page))
            # all done
            return self

        def help(self, entry: journal.entry) -> "Capture":
            """
            Keep the page of a help {entry}
            """
            # save the page
            seen.append(list(entry.page))
            # all done
            return self

        def memo(self, entry: journal.entry) -> "Capture":
            """
            Keep the page of a developer facing {entry}
            """
            # save the page
            seen.append(list(entry.page))
            # all done
            return self

    # work in a scratch area
    with tempfile.TemporaryDirectory() as scratch:
        # go there
        os.chdir(scratch)
        # hide the configuration files that might give git an identity
        os.environ.update(HOME=scratch, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1")
        # and the variables that might do the same
        for name in (
            "GIT_AUTHOR_NAME",
            "GIT_AUTHOR_EMAIL",
            "GIT_COMMITTER_NAME",
            "GIT_COMMITTER_EMAIL",
            "EMAIL",
        ):
            # by removing them
            os.environ.pop(name, None)
        # and keep git from guessing one from the name of the host
        os.environ.update(
            GIT_CONFIG_COUNT="1",
            GIT_CONFIG_KEY_0="user.useConfigOnly",
            GIT_CONFIG_VALUE_0="true",
        )
        # make a device for the complaint
        capture = Capture()
        # and route the error channel of smith to it
        journal.error("smith").device = capture
        # make the app, with a project that spells everything the templates ask for
        app = pyre.smith.smith(name="smith_git_identity")
        app.project = "basic"
        app.project.name = "hello"
        app.project.authors = "the authors"
        app.project.span = "2026"
        app.project.github = "authors/hello"
        # silence the progress report, since what matters is the outcome
        journal.info("smith").deactivate()
        # generate the project
        status = app.run()
        # it did not claim success
        assert status != 0
        # the project was assembled all the same
        assert (pyre.primitives.path("hello") / "share" / "hello" / "hello.yaml").exists()
        # there was exactly one complaint
        assert len(seen) == 1
        # get its page
        page = seen[0]
        # it says that the project was assembled
        assert page[0] == (
            "the project 'hello' was assembled, but could not be placed under source control"
        )
        # names the step that failed
        assert page[1].startswith("while running 'git commit")
        # and quotes git
        assert len(page) > 2
    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
