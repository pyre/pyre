#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a package deduces its installation prefix from the location of its importable, in
the pyre layout and in the layout pip and conda use
"""

# support
import pyre


def test():
    # for the scratch layouts
    import os
    import tempfile

    # the executive
    executive = pyre.executive
    # a scratch area; the package resolves its location, so resolve the scratch area too, in
    # case the temporary directory sits behind a symbolic link, as it does on macOS
    with tempfile.TemporaryDirectory() as scratch:
        scratch = pyre.primitives.path(scratch).resolve()
        # the pyre layout: {prefix}/packages/{package}/__init__.py
        prefix = scratch / "pyre-layout"
        home = prefix / "packages" / "layout_pyre"
        os.makedirs(home)
        # the package configuration folder
        os.makedirs(prefix / "share" / "layout_pyre")
        # register the package
        package = executive.registerPackage(name="layout_pyre", file=home / "__init__.py")
        # the prefix is two levels up from the package
        assert package.prefix == prefix
        # and the configuration folder was found under {share}
        assert package.config == prefix / "share" / "layout_pyre"

        # the site-packages layout: {prefix}/lib/pythonX.Y/site-packages/{package}/__init__.py
        prefix = scratch / "conda-layout"
        home = prefix / "lib" / "python3.14" / "site-packages" / "layout_conda"
        os.makedirs(home)
        # the package configuration folder
        os.makedirs(prefix / "share" / "layout_conda")
        # register the package
        package = executive.registerPackage(name="layout_conda", file=home / "__init__.py")
        # the prefix is four levels up from the package, not two
        assert package.prefix == prefix
        # and the configuration folder was found under {share}
        assert package.config == prefix / "share" / "layout_conda"
    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
