#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a recipe never records an owned part by its name: reading a facility stamps its
slot, so the binding looks configured, and a specification that carries the name of the part
leads the loader back to the slot it is trying to bind
"""

# support
import pyre


# a protocol
class Gadget(pyre.protocol, family="recipe.gadgets"):
    """
    Gadgets
    """

    @classmethod
    def pyre_default(cls, **kwds):
        """
        The default gadget
        """
        # a widget
        return Widget


# a part, meant to be owned
class Widget(pyre.component, family="recipe.gadgets.widget", implements=Gadget):
    """
    A widget
    """

    level = pyre.properties.int(default=1)


# the owner
class Holder(pyre.component, family="recipe.holder"):
    """
    A holder of gadgets
    """

    gadget = Gadget()


def test():
    # make a holder
    holder = Holder(name="recipe.holder")
    # read its part, the way any client would before persisting
    gadget = holder.gadget
    # configure the part
    gadget.level = 5
    # build the recipe
    recipe = pyre.config.newRecipe().add(holder)
    # the binding is recorded by family alone, never by the name of the part
    assert recipe.section("recipe.holder") == {"gadget": "recipe.gadgets.widget"}
    # and the part has its section
    assert recipe.section("recipe.holder.gadget") == {"level": 5}

    # the loader must be able to bind what the recipe recorded: configure another holder
    # with the same section
    pyre.executive.nameserver["recipe.other.gadget"] = recipe.section("recipe.holder")["gadget"]
    # build it
    other = Holder(name="recipe.other")
    # and check that its part is what the recipe said
    assert isinstance(other.gadget, Widget)
    assert other.gadget.pyre_name == "recipe.other.gadget"
    # all done
    return recipe


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
