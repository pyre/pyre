#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a recipe can be pickled: it arrives with its sections and the families of its
components, and without the components, which belong to the process that described them
"""

# externals
import pickle

# support
import pyre


# a component
class Gadget(pyre.component, family="recipe.pickle.gadget"):
    """
    A gadget
    """

    # a number
    level = pyre.properties.int(default=1)


def test():
    # build a gadget, configured at construction
    gadget = Gadget(name="recipe.pickle.sample", level=5)
    # describe it
    recipe = pyre.config.newRecipe().add(gadget)
    # send it on a round trip
    copy = pickle.loads(pickle.dumps(recipe))
    # the sections arrived
    assert copy.sections == recipe.sections
    # and so did the families
    assert copy.families == recipe.families
    # but not the components
    assert copy.components == {}
    # which the original still has
    assert recipe.components == {"recipe.pickle.sample": gadget}
    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
