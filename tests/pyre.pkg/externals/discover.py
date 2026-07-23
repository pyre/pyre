#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Select a package through the framework, driven entirely by YAML configuration

The configuration file {discover.yaml} restricts the host to the bare engine and points its
search path at the fixture installation, so this test runs the full facility resolution path
on any host
"""

# support
import pyre


# the application
class discover(pyre.application):
    """
    An application with an external package requirement
    """

    # the requirement
    gsl = pyre.externals.gsl()
    gsl.doc = "the GSL installation"


def test():
    """
    Resolve the gsl facility and verify the discovered configuration
    """
    # instantiate the application; this loads {discover.yaml}
    app = discover(name="discover")
    # get the selected installation
    gsl = app.gsl
    # the fixture must have been found
    assert gsl is not None
    # the discovery populated the traits from the fixture
    assert [str(folder) for folder in gsl.incdir] == ["prefix/include"]
    assert [str(folder) for folder in gsl.libdir] == ["prefix/lib"]
    assert list(gsl.libraries) == ["gsl", "gslcblas"]
    # the configuration must be valid: the folders exist
    assert not gsl.pyre_configurationErrors
    # and the provenance must point at the discovery
    assert "bare" in str(gsl.pyre_where(attribute="incdir"))
    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
