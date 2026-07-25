#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise the macports engine against a canned database

The scenarios cover the {port select} machinery: the selected alternative usually names the
payload port directly, while on modern macports the selection files belong to {_select}
metadata ports that the recipe markers must reject; and version-tagged port names like
{py312-numpy} that only a pattern can reach
"""

# the fake database, modeled on an actual macports host
installed = {
    # the python payload and its selection metadata
    "python314": ("3.14.6", set()),
    "python3_select-314": ("3.14.6", set()),
    "python3_select": ("0.1", set()),
    # a version-tagged port that only a pattern can reach
    "py312-numpy": ("2.3.4", set()),
}

# the contents of each package
contents = {
    # the payload
    "python314": [
        "/opt/local/Library/Frameworks/Python.framework/Versions/3.14/bin/python3.14",
        "/opt/local/Library/Frameworks/Python.framework/Versions/3.14/include/python3.14/Python.h",
        "/opt/local/Library/Frameworks/Python.framework/Versions/3.14/lib/libpython3.14.dylib",
    ],
    # the selection metadata: no development artifacts
    "python3_select-314": ["/opt/local/etc/select/python3/python314"],
    "python3_select": ["/opt/local/etc/select/python3/base"],
    # the version-tagged port
    "py312-numpy": [
        "/opt/local/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12"
        "/site-packages/numpy/_core/include/numpy/arrayobject.h",
    ],
}

# the selection state: group -> ranked alternatives, selection first
alternatives = {
    "python3": ("python314",),
}


def test():
    """
    Configure python and numpy recipes against the canned database
    """
    # support
    import pyre

    # the engine to fake
    from pyre.platforms.MacPorts import MacPorts

    # the categories
    from pyre.externals.Python import Python
    from pyre.externals.NumPy import NumPy

    # an engine wired to the canned database instead of a port client
    class engine(MacPorts):
        """
        A macports engine over canned data
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

        # the selection state
        def getAlternatives(self):
            """
            Serve the canned selection state
            """
            # easy enough
            return alternatives

        # the selection file provider
        def getSelectionInfo(self, group, alternative):
            """
            Pretend the selection files belong to the {_select} metadata port
            """
            # the modern macports arrangement
            return f"{group}_select-314"

    # instantiate
    macports = engine(name="macports.fake")

    # get the python recipe
    recipe, *_ = Python.recipes()
    # the payload port must win the resolution
    assert macports.resolve(recipe=recipe) == "python314"
    # interpret it
    values = macports.configure(recipe=recipe)
    # the discovery must succeed
    assert values is not None
    # with the version of the payload port
    assert values["version"] == "3.14.6"
    # the actual library stem
    assert values["libraries"] == ["python3.14"]
    # and the interpreter
    assert values["interpreter"] == "python3.14"

    # get the numpy recipe
    numpy, *_ = NumPy.recipes()
    # only the pattern can reach the version-tagged port
    assert macports.resolve(recipe=numpy) == "py312-numpy"
    # interpret it
    values = macports.configure(recipe=numpy)
    # the discovery must succeed
    assert values is not None
    # with the headers wherever the site packages put them
    assert [str(f) for f in values["incdir"]] == [
        "/opt/local/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12"
        "/site-packages/numpy/_core/include"
    ]

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
