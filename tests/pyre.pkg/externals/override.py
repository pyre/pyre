#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that user configuration overrides discovered values

The configuration file {override.yaml} pins the version of the gsl installation; the
discovery deposits its own version at lower priority and must lose the arbitration
"""

# support
import pyre


# the application
class override(pyre.application):
    """
    An application with an external package requirement
    """

    # the requirement
    gsl = pyre.externals.gsl()
    gsl.doc = "the GSL installation"


def test():
    """
    Resolve the gsl facility and verify that the user setting wins
    """
    # instantiate the application; this loads {override.yaml}
    app = override(name="override")
    # get the selected installation
    gsl = app.gsl
    # the fixture must have been found
    assert gsl is not None
    # the user pinned the version
    assert gsl.version == "9.9-custom"
    # and the provenance must not claim the value came from package discovery
    assert "package database" not in str(gsl.pyre_where(attribute="version"))
    # while undisturbed traits still carry the discovered values
    assert [str(folder) for folder in gsl.incdir] == ["prefix/include"]
    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
