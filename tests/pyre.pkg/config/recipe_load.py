#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a recipe loaded in another process configures the component built there by the name
it records, and leaves the defaults to the code
"""

# externals
import multiprocessing

# support
import pyre


# a component with a configured trait and one left at its default
class Gadget(pyre.component, family="recipe.load.gadget"):
    """
    A gadget
    """

    # a number
    level = pyre.properties.int(default=1)
    # and some text
    label = pyre.properties.str(default="gadget")


def rebuild(recipe):
    """
    Load {recipe} in this process, and report the configuration of the gadget it describes
    """
    # load the recipe
    pyre.loadRecipe(recipe)
    # build the gadget by its recorded name
    gadget = Gadget(name="recipe.load.sample")
    # and report what it got
    return gadget.level, gadget.label


def test():
    # build a gadget, configured at construction
    gadget = Gadget(name="recipe.load.sample", level=5)
    # describe it
    recipe = pyre.config.newRecipe().add(gadget)
    # start a process that inherits nothing from this one
    context = multiprocessing.get_context("spawn")
    # with a single worker
    with context.Pool(processes=1) as pool:
        # rebuild the gadget there
        level, label = pool.apply(rebuild, kwds={"recipe": recipe})
    # the configured trait came along
    assert level == 5
    # and the default came from the code
    assert label == "gadget"
    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
