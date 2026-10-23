#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that smith finds its templates in the installation and generates a project from the
basic one, with every macro in the templates resolved
"""

# support
import journal
import pyre.smith


def test():
    """
    Generate a project from the basic template and check its configuration file
    """
    # for the scratch area
    import os
    import tempfile

    # give git an identity, so the initial revision can be recorded wherever the test runs
    os.environ.update(
        GIT_AUTHOR_NAME="pyre tests",
        GIT_AUTHOR_EMAIL="tests@pyre.invalid",
        GIT_COMMITTER_NAME="pyre tests",
        GIT_COMMITTER_EMAIL="tests@pyre.invalid",
    )

    # the templates live in the installation, under {share/pyre}
    vault = pyre.prefix / "share" / "pyre" / "templates" / "basic"
    # make sure they are there
    assert vault.isDirectory(), f"no templates at {vault}"
    # work in a scratch area
    with tempfile.TemporaryDirectory() as scratch:
        # go there
        os.chdir(scratch)
        # make the app, with a project that spells everything the templates ask for
        app = pyre.smith.smith(name="smith_basic")
        # built from the basic template
        app.project = "basic"
        # named after the traditional greeting
        app.project.name = "hello"
        # with its authors
        app.project.authors = "the authors"
        # the years of its copyright
        app.project.span = "2026"
        # and its repository
        app.project.github = "authors/hello"
        # silence the progress report, since what matters is the generated tree
        journal.info("smith").deactivate()
        # generate the project
        status = app.run()
        # it went well
        assert status == 0
        # the project configuration file
        config = pyre.primitives.path("hello") / "share" / "hello" / "hello.yaml"
        # was generated
        assert config.exists()
        # read it
        text = config.open().read()
        # with every macro resolved
        assert "{project." not in text
        # the name capitalized, as derived from the name
        assert "capname: Hello" in text
        # and the repository as given
        assert "github: authors/hello" in text
    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
