#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A package whose split off executable is absent verifies clean

Discovery admits a package with headers and libraries even when its executables are
missing, since package managers routinely ship the client separately; conda's {libpq} is
the live example. Verification must not condemn what discovery deliberately admitted
"""

# the fake database: the client library without the client program
installed = {
    # the development package
    "libpq-dev": ("18.3", "1"),
}

# the contents of each package; the paths are anchored in the test fixture so that the
# configured directories exist and the installation validates
contents = {
    # headers and library, but no {psql}
    "libpq-dev": ["prefix/include/libpq-fe.h", "prefix/lib/libpq.dylib"],
}


def test():
    """
    Verify a postgres installation that carries no client executable
    """
    # the engine to fake
    from pyre.platforms.DPkg import DPkg

    # the index class
    from pyre.externals.Index import Index

    # an engine wired to the fake database instead of a dpkg client
    class engine(DPkg):
        """
        A dpkg engine over canned data
        """

        # the installed package index
        def getInstalledPackages(self):
            """
            Serve the canned index
            """
            # easy enough
            return installed

        # package contents
        def retrievePackageContents(self, package):
            """
            Serve the canned contents
            """
            # easy enough
            yield from contents[package]
            # all done
            return

    # make a private index over the fake engine
    index = Index()
    # wire it
    index._engines = (engine(name="dpkg.fake.verify.optional"),)
    # resolve
    report = index.resolve(requested=["postgresql"])
    # the library was discovered despite the missing client
    assert "postgresql" in report.selections
    # and the client trait fell back to its default, naming a program that isn't there
    assert report.selections["postgresql"].psql == "psql"

    # verify the outcome
    audit = index.verify(report=report)
    # the installation checks out: its headers and libraries are all present, and the
    # executable was never a hard marker for a package that carries them
    assert audit.verified == ["postgresql"]
    # so nothing is broken
    assert not audit.broken

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
