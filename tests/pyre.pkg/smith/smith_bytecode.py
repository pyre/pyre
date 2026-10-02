#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that smith leaves behind the bytecode an installer compiled next to the template sources,
as pip does when it installs a wheel
"""

# support
import journal
import pyre
import pyre.smith

# the application class, which the package publishes through a factory
from pyre.smith.Smith import Smith as Base


def test():
    # for the scratch area
    import os
    import shutil
    import tempfile

    # the templates live in the installation, under {share/pyre}
    basic = pyre.prefix / "share" / "pyre" / "templates" / "basic"
    # make sure they are there
    assert basic.isDirectory(), f"no templates at {basic}"
    # work in a scratch area
    with tempfile.TemporaryDirectory() as scratch:
        # go there
        os.chdir(scratch)
        # copy the basic template, so the installation stays untouched
        copy = shutil.copytree(str(basic), os.path.join(scratch, "vault"))
        # make a bytecode cache in it, where an installer would put one
        cache = os.path.join(copy, "__pycache__")
        os.mkdir(cache)
        # with a file that is not text, as compiled bytecode is not
        with open(os.path.join(cache, "meta.cpython-313.pyc"), "wb") as stream:
            # starting with the bytes that broke smith
            stream.write(b"\xf3\r\r\n\x00\x00\x00\x00")

        # a smith that draws from the copy
        # with a family of its own, so it is public and knows its package, as applications do
        class Smith(Base, family="pyre.applications.smith.bytecode"):
            """
            A smith whose template is the scratch copy of the basic one
            """

            # the location of the template
            @property
            def vault(self):
                """
                Point to the scratch copy
                """
                # the copy with the bytecode in it
                return pyre.primitives.path(copy)

        # make the app, with a project that spells everything the templates ask for
        app = Smith(name="smith_bytecode")
        app.project = "basic"
        app.project.name = "hello"
        app.project.authors = "the authors"
        app.project.span = "2026"
        app.project.github = "authors/hello"
        # silence the progress report, since what matters is the generated tree
        journal.info("smith").deactivate()
        # generate the project
        status = app.run()
        # it went well
        assert status == 0
        # the generation got all the way to the project configuration file
        assert (pyre.primitives.path("hello") / "share" / "hello" / "hello.yaml").exists()
        # and the bytecode cache stayed behind
        assert not (pyre.primitives.path("hello") / "__pycache__").exists()
    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
