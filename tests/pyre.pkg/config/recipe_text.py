#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a recipe records the values that travel as text in a form that loading reads back
"""

# support
import enum
import pyre


# an enumeration
class Band(enum.Enum):
    """
    The radar bands
    """

    # the members
    L = 1
    # and the one above it
    S = 2


# a component with values that travel as text
class Radar(pyre.component, family="recipe.text.radar"):
    """
    A radar with a band, a cell type, a socket, a complex gain and a set of modes
    """

    # the band
    band = pyre.properties.enum(enum=Band)
    # the type of its samples
    sample = pyre.properties.cell()
    # the socket it reports to
    socket = pyre.properties.inet()
    # its gain
    gain = pyre.properties.complex()
    # and its modes
    modes = pyre.properties.set(schema=pyre.properties.str())


def test():
    """
    Persist a radar and build another one out of what was written
    """
    # support
    from pyre.config.yaml import editor

    # if the backend is not available
    if not editor.available():
        # there is nothing to check
        return None
    # the file with the state; it does not exist yet
    uri = pyre.primitives.path("recipe_text.yaml")
    # make sure
    if uri.exists():
        # by removing leftovers from an earlier run
        uri.unlink()
    # build a radar
    radar = Radar(name="recipe.text.original")
    # in the S band
    radar.band = Band.S
    # with complex samples
    radar.sample = "complex64"
    # reporting to a unix socket
    radar.socket = "unix:/tmp/radar.socket"
    # with a gain
    radar.gain = 1 + 2j
    # and two modes, one with literal braces, which assignment would otherwise interpolate
    radar.modes = {"dbf", "{{ss}}"}
    # persist it
    radar.pyre_persist(uri=uri)
    # a second radar, configured by what the first one wrote
    doc = pyre.config.newYamlEditor(uri=uri)
    # under a name of its own
    doc.set("recipe.text.copy", value=doc.get("recipe.text.original"))
    # saved with the rest
    doc.save()
    # restoring is plain configuration
    pyre.loadConfiguration(str(uri))
    # build the copy
    copy = Radar(name="recipe.text.copy")
    # its band is the same
    assert copy.band is Band.S, copy.band
    # and so is its cell type
    assert copy.sample is pyre.memory.cells.complexFloat, copy.sample
    # its socket is a unix socket
    assert isinstance(copy.socket, pyre.schemata.inet.unix), copy.socket
    # at the same path
    assert copy.socket.path == "/tmp/radar.socket", copy.socket.path
    # its gain is the same
    assert copy.gain == 1 + 2j, copy.gain
    # and so are its modes, braces and all
    assert copy.modes == {"dbf", "{ss}"}, copy.modes

    # all done
    return radar


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
