#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a recipe loaded in another process binds the facilities of the component built there
to components configured as the recipe describes them: a part the component owns, and a shared
component bound by name
"""

# externals
import multiprocessing

# support
import pyre


# a protocol
class Thing(pyre.protocol, family="recipe.load.things"):
    """
    Things
    """

    @classmethod
    def pyre_default(cls, **kwds):
        """
        The default thing
        """
        # a part
        return Part


# a part, meant to be owned
class Part(pyre.component, family="recipe.load.things.part", implements=Thing):
    """
    A part
    """

    # a number
    level = pyre.properties.int(default=1)


# a shared component
class Shared(pyre.component, family="recipe.load.things.shared", implements=Thing):
    """
    A shared thing
    """

    # a number
    level = pyre.properties.int(default=0)


# the owner
class Owner(pyre.component, family="recipe.load.owner"):
    """
    An owner of things
    """

    # a component bound by default
    part = Thing()
    # and one that is not
    friend = Thing()
    # since it starts out empty
    friend.default = None


def rebuild(recipe):
    """
    Load {recipe} in this process, and report the configuration of the owner it describes
    """
    # load the recipe
    pyre.loadRecipe(recipe)
    # build the owner by its recorded name
    owner = Owner(name="recipe.load.keeper")
    # and report what its facilities got
    return (
        type(owner.part).__name__,
        owner.part.level,
        type(owner.friend).__name__,
        owner.friend.pyre_name,
        owner.friend.level,
    )


def test():
    # a shared thing, configured at construction
    shared = Shared(name="recipe.load.shared", level=3)
    # the owner, with its friend bound to the shared thing
    owner = Owner(name="recipe.load.keeper", friend=shared)
    # and its part configured
    owner.part.level = 7
    # describe it
    recipe = pyre.config.newRecipe().add(owner)
    # start a process that inherits nothing from this one
    context = multiprocessing.get_context("spawn")
    # with a single worker
    with context.Pool(processes=1) as pool:
        # rebuild the owner there
        report = pool.apply(rebuild, kwds={"recipe": recipe})
    # the part came back with its configuration, and the friend is the shared thing, by name
    assert report == ("Part", 7, "Shared", "recipe.load.shared", 3)
    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
