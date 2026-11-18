#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre


# a component with text in a string, a map and a list
class Card(pyre.component, family="recipe.braces.card"):
    """
    A card with labels
    """

    # a label
    label = pyre.properties.str()
    # some tags
    tags = pyre.properties.kv()
    # and some notes
    notes = pyre.properties.list(schema=pyre.properties.str())


def test():
    """
    Check that text with braces survives being persisted and read back: a configuration file is
    interpolated when it is read, so the recipe writes the braces of the values it records escaped
    """
    # support
    from pyre.config.yaml import editor

    # if the backend is not available
    if not editor.available():
        # there is nothing to check
        return None

    # the file with the state; it does not exist yet
    uri = pyre.primitives.path("recipe_braces.yaml")
    # make sure
    if uri.exists():
        # by removing leftovers from an earlier run
        uri.unlink()

    # build a card
    card = Card(name="recipe.braces.saved")
    # and give it text with literal braces, empty pairs, and the rendering of a dictionary
    card.label = "{{band}}"
    card.tags = {"band": "{{L}}", "empty": "{}", "table": "{{'k': 'v'}}"}
    card.notes = ["{{a}}", "b}}{{c"]
    # which hold them literally: the label
    assert card.label == "{band}"
    # the tags
    assert dict(card.tags) == {"band": "{L}", "empty": "{}", "table": "{'k': 'v'}"}
    # and the notes
    assert list(card.notes) == ["{a}", "b}{c"]
    # persist it
    pyre.saveConfiguration(uri=uri, components=[card])

    # open the file
    doc = pyre.config.newYamlEditor(uri=uri)
    # which escapes the braces of the text it holds
    assert doc.get("recipe.braces.saved", "label") == "{{band}}"
    # a second card, configured by what the first one wrote
    doc.set("recipe.braces.copy", value=doc.get("recipe.braces.saved"))
    # goes in the same file
    doc.save()
    # restoring is plain configuration
    pyre.loadConfiguration(str(uri))
    # build the copy
    copy = Card(name="recipe.braces.copy")
    # and check that it came up with the same text: the label
    assert copy.label == card.label
    # the tags
    assert dict(copy.tags) == dict(card.tags)
    # and the notes
    assert list(copy.notes) == list(card.notes)

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
