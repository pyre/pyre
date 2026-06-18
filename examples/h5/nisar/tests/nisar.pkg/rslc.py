#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify the RSLC product schema: the L-band mount, the constrained identification, the
optional frequency sub-bands and polarization channels, and the shared SLC datum
"""


# the driver
def test():
    # support
    import journal
    from nisar.schema.rslc import rslc
    from pyre.constraints.exceptions import ConstraintViolationError

    # build the product specification
    spec = rslc(name="root")

    # it mounts at the L-band root
    assert spec._pyre_location == "/science/LSAR"

    # and, being rooted at {schema.Root}, it carries an index of named shape dimensions
    assert spec._pyre_shapes is not None

    # identification: mission default and the fixed product type
    ident = spec._pyre_find("identification")
    assert ident._pyre_get("missionId").default == "NISAR"
    assert ident._pyre_get("productType").default == "RSLC"

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

    # the azimuth dimension is shared, declared on the swaths group
    assert "nlines" in spec._pyre_find("RSLC/swaths")._pyre_classDimensions

    # both frequency sub-bands are declared in the swaths group and are optional
    for f in ("frequencyA", "frequencyB"):
        assert spec._pyre_find(f"RSLC/swaths/{f}")._pyre_optional is True

    # a frequency provides the per-frequency range dimension
    freqA = spec._pyre_find("RSLC/swaths/frequencyA")
    assert "nsamples" in freqA._pyre_classDimensions
    # and carries a constrained polarization list and optional SLC channels
    assert freqA._pyre_get("listOfPolarizations").constraints
    for pol in ("HH", "HV", "VH", "VV"):
        channel = freqA._pyre_get(pol)
        assert channel._pyre_optional is True
        assert channel._pyre_marker() == "array[complex]"

    # the radar-geometry coordinate axis, per-frequency
    assert spec._pyre_find("RSLC/swaths/frequencyA/slantRange")._pyre_marker() == "array[float]"

    # offer a structural visualization on a debug channel the user can activate
    spec._pyre_view(channel=journal.debug("nisar.schema.rslc"))

    # all done
    return


# main
if __name__ == "__main__":
    # drive
    test()


# end of file
