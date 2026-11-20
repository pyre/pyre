#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the description of a component shows the defaults of its traits as they were declared:
text as written, expressions included, and other values in the text their schema reads back
"""


def test() -> None:
    """
    Describe a component whose traits declare their defaults in every form
    """
    # support
    import json
    import pyre

    # a component with defaults declared as text, as expressions, and as values
    class Radar(pyre.component, family="pyre.tests.describe.defaults.radar"):
        """
        A component with declared defaults
        """

        # a cell type, named by text
        cell = pyre.properties.cell(default="float64")
        # a complex gain, written as text
        gain = pyre.properties.complex(default="1+2j")
        # a number of channels
        channels = pyre.properties.int(default=3)
        # a number of looks that follows the number of channels
        looks = pyre.properties.int(default="{radar.channels}")
        # the cell types of the layers, given as a list of names
        layers = pyre.properties.list(schema=pyre.properties.cell(), default=["uint8", "complex64"])
        # the servers, given as a table of address text
        servers = pyre.properties.dict(
            schema=pyre.properties.inet(), default={"db": "unix:/var/run/db.sock"}
        )
        # a cell type nobody declared
        output = pyre.properties.cell()
        # and a secret with a default
        token = pyre.properties.str(default="hunter2")
        token.secret = True

    # make one
    radar = Radar(name="radar")
    # describe it
    doc = radar.pyre_renderConfiguration()
    # the description can be written as json
    text = json.dumps(doc)
    # get the descriptions of the properties
    properties = doc["properties"]

    # text defaults are shown as they were written
    assert properties["cell"]["default"] == "float64"
    # complex numbers included
    assert properties["gain"]["default"] == "1+2j"
    # expressions included
    assert properties["looks"]["default"] == "{radar.channels}"
    # while the value of the trait is the one the expression evaluates to
    assert properties["looks"]["value"] == 3
    # numbers stay numbers
    assert properties["channels"]["default"] == 3
    # containers are shown with each entry in the text its schema reads back, lists
    assert properties["layers"]["default"] == ["uint8", "complex64"]
    # and tables
    assert properties["servers"]["default"] == {"db": "unix:/var/run/db.sock"}
    # a trait without a default shows none
    assert properties["output"]["default"] is None
    # secrets keep their defaults out of the description
    assert properties["token"]["default"] is None
    # and out of the text of the description
    assert "hunter2" not in text

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
