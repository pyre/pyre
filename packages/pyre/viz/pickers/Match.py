# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the protocol
from ..protocols.Picker import Picker

# the specifications of my slots
from ..protocols.Contents import Contents
from ..protocols.Dataset import Dataset


# pick the dataset whose value along every axis is the selected one
class Match(pyre.flow.factory, family="pyre.viz.pickers.match", implements=Picker):
    """
    Pick the dataset of a file whose value along every axis of its contents is the one in my
    selection; a selection that leaves an axis out, or that no dataset matches, makes nothing
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

    # framework hooks
    def pyre_suggest(self, trait):
        """
        Suggest the selections that pick a dataset, one for every dataset in my contents, which
        are pulled from my reader to find out; i have no suggestions for my other traits
        """
        # for anything other than my selection
        if trait.name != "selection":
            # defer to the framework
            yield from super().pyre_suggest(trait=trait)
            # and stop
            return
        # get my contents
        contents = self.contents
        # if nothing is bound to them
        if contents is None:
            # there is nothing to go on
            return
        # make sure they are up to date, which asks my reader to fill them
        contents.pyre_make()
        # every dataset in them can be picked by its value along every axis
        for entry in contents.entries:
            # so suggest it
            yield dict(entry["selector"])
        # all done
        return

    # flow hooks
    def pyre_run(self, **kwds):
        """
        Pick the dataset that matches my selection out of my contents
        """
        # get a selector from my contents
        selector = self.contents.selector()
        # and my selection
        selection = dict(self.selection)
        # find out whether it picks a dataset
        reason = selector.refusal(selection=selection)
        # if it doesn't
        if reason is not None:
            # nothing can be made, for the reason the selector gives
            raise self.ProductionError(node=self, product="dataset", reason=reason)
        # otherwise, get the dataset it picks
        entry = selector.pick(selection=selection)
        # fill my output with it
        self.dataset.fill(selector=entry["selector"], source=entry.get("source"))
        # and chain up
        return super().pyre_run(**kwds)


# end of file
