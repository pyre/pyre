#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that text with braces comes back as it was when a recipe is loaded in another process: the
configuration store interpolates what it holds, so the recipe carries the braces escaped
"""

# externals
import multiprocessing

# support
import pyre


# a component with text in a string, a map and a list
class Card(pyre.component, family="recipe.load.braces.card"):
    """
    A card with labels
    """

    # a label
    label = pyre.properties.str()
    # some tags
    tags = pyre.properties.kv()
    # and some notes
    notes = pyre.properties.list(schema=pyre.properties.str())


def rebuild(recipe):
    """
    Load {recipe} in this process, and report the text of the card it describes
    """
    # load the recipe
    pyre.loadRecipe(recipe)
    # build the card by its recorded name
    card = Card(name="recipe.load.braces.sample")
    # and report its text
    return card.label, dict(card.tags), list(card.notes)


def test():
    # build a card
    card = Card(name="recipe.load.braces.sample")
    # and give it text with literal braces, empty pairs, and the rendering of a dictionary
    card.label = "{{band}}"
    card.tags = {"band": "{{L}}", "empty": "{}", "table": "{{'k': 'v'}}"}
    card.notes = ["{{a}}", "b}}{{c"]
    # describe it
    recipe = pyre.config.newRecipe().add(card)
    # start a process that inherits nothing from this one
    context = multiprocessing.get_context("spawn")
    # with a single worker
    with context.Pool(processes=1) as pool:
        # rebuild the card there
        label, tags, notes = pool.apply(rebuild, kwds={"recipe": recipe})
    # the label came back as it was
    assert label == card.label
    # and so did the tags
    assert tags == dict(card.tags)
    # and the notes
    assert notes == list(card.notes)
    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
