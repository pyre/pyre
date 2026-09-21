#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a recipe always records the binding of an owned part, by family and never by
name: a specification that carries the name of the part leads the loader back to the slot it
is trying to bind. Components without a family stay out of recipes, and asking for the
recipe of one is an error
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


# a component class without a family
class Loner(pyre.component, implements=Gadget):
    """
    A gadget that stays outside the configuration store
    """

    level = pyre.properties.int(default=1)


def test():
    # a holder nobody has looked into
    fresh = Holder(name="recipe.fresh")
    # records the binding of its part, even though it came from the default
    assert pyre.config.newRecipe().add(fresh).section("recipe.fresh") == {
        "gadget": "recipe.gadgets.widget"
    }

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

    # a holder bound to a gadget without a family
    private = Holder(name="recipe.private", gadget=Loner(name="recipe.loner"))
    # describes itself
    recipe = pyre.config.newRecipe().add(private)
    # and leaves the gadget out, since no configuration file can say how to rebuild it
    assert recipe.section("recipe.private") == {}
    assert recipe.section("recipe.loner") is None
    # asking for the recipe of the gadget itself
    try:
        # is an error
        pyre.config.newRecipe().add(private.gadget)
        # so we should not get here
        assert False, "unreachable"
    # if all goes well
    except pyre.config.exceptions.PersistenceError as error:
        # check that the report names the culprit
        assert error.component is private.gadget
    # and so is persisting it
    try:
        # which must fail before it touches the file system
        private.gadget.pyre_persist(uri="recipe-unreachable.yaml")
        # so we should not get here
        assert False, "unreachable"
    # if all goes well
    except pyre.config.exceptions.PersistenceError:
        # check that no file was made
        assert not pyre.primitives.path("recipe-unreachable.yaml").exists()

    # all done
    return recipe


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
