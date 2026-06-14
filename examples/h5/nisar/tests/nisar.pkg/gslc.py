#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify the GSLC product schema: the L-band mount, the constrained identification, the
optional frequency sub-bands and polarization channels, and the shared SLC datum
"""


# the driver
def test():
    # support
    import journal
    from nisar.products.gslc import gslc
    from pyre.constraints.exceptions import ConstraintViolationError

    # build the product specification
    spec = gslc(name="root")

    # it mounts at the L-band root
    assert spec._pyre_location == "/science/LSAR"

    # identification: mission default and the fixed product type
    ident = spec._pyre_find("identification")
    assert ident._pyre_get("missionId").default == "NISAR"
    assert ident._pyre_get("productType").default == "GSLC"

    # listOfFrequencies is constrained to a non-empty subset of {"A", "B"}
    freqs = ident._pyre_get("listOfFrequencies")
    assert freqs.constraints
    assert freqs.process(value=["A"]) == ["A"]
    for bad in (["A", "C"], []):
        try:
            freqs.process(value=bad)
            assert False, "expected a constraint violation"
        except ConstraintViolationError:
            pass

    # both frequency sub-bands are declared in the grids group and are optional
    for f in ("frequencyA", "frequencyB"):
        assert spec._pyre_find(f"GSLC/grids/{f}")._pyre_optional is True

    # a frequency carries a constrained polarization list and optional SLC channels
    freqA = spec._pyre_find("GSLC/grids/frequencyA")
    assert freqA._pyre_get("listOfPolarizations").constraints
    for pol in ("HH", "HV", "VH", "VV"):
        channel = freqA._pyre_get(pol)
        assert channel._pyre_optional is True
        assert channel._pyre_marker() == "array[complex]"

    # the map-projection coordinate axis
    assert spec._pyre_find("GSLC/grids/xCoordinates")._pyre_marker() == "array[float]"

    # offer a structural visualization on a debug channel the user can activate
    spec._pyre_view(channel=journal.debug("nisar.products.gslc"))

    # all done
    return


# main
if __name__ == "__main__":
    # drive
    test()


# end of file
