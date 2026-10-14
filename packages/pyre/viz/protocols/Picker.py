# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the specifications of my slots
from .Contents import Contents
from .Dataset import Dataset


# the protocol of the factories that pick one of the datasets of a file
class Picker(pyre.flow.producer, family="pyre.viz.pickers"):
    """
    The picker protocol: read the contents of a file and write the dataset whose value along
    every axis is the one in {selection}
    """

    # user configurable state
    selection = pyre.properties.kv()
    selection.doc = "the value of the dataset to pick along every axis of the contents"

    # the input
    contents = Contents.input()
    contents.doc = "what the reader found in its file"

    # the output
    dataset = Dataset.output()
    dataset.doc = "the dataset that matches the selection"


# end of file
