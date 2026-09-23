#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that smith finds its templates in the installation and generates a project from the
basic one, with every macro in the templates resolved
"""

# support
import pyre
import pyre.smith


def test():
    # for the scratch area
    import os
    import tempfile

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
        app.project = "basic"
        app.project.name = "hello"
        app.project.authors = "the authors"
        app.project.span = "2026"
        app.project.github = "authors/hello"
        # generate the project
        status = app.run()
        # it went well
        assert status == 0
        # the project configuration file was generated
        config = pyre.primitives.path("hello") / "share" / "hello" / "hello.yaml"
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
