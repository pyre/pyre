#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a package installed in the dist-packages folder of the debian and ubuntu system python
deduces its installation prefix
"""

# support
import pyre


def test():
    """
    Register a package that lives in {dist-packages} and check its prefix and configuration folder
    """
    # for the scratch layout
    import os
    import tempfile

    # the executive
    executive = pyre.executive
    # a scratch area; the package resolves its location, so resolve the scratch area too, in
    # case the temporary directory sits behind a symbolic link, as it does on macOS
    with tempfile.TemporaryDirectory() as scratch:
        # resolve it
        scratch = pyre.primitives.path(scratch).resolve()
        # the layout: {prefix}/lib/pythonX.Y/dist-packages/{package}/__init__.py
        prefix = scratch / "debian-layout"
        # the home of the package
        home = prefix / "lib" / "python3.14" / "dist-packages" / "layout_debian"
        # make it
        os.makedirs(home)
        # and the package configuration folder
        os.makedirs(prefix / "share" / "layout_debian")
        # register the package
        package = executive.registerPackage(name="layout_debian", file=home / "__init__.py")
        # the prefix is four levels up from the package, not two
        assert package.prefix == prefix
        # and the configuration folder was found under {share}
        assert package.config == prefix / "share" / "layout_debian"

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
