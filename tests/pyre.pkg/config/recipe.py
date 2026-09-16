#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a recipe says what was configured and nothing else: properties set in a file or
at construction appear as plain values, defaults are left out, owned parts get their own
sections, shared components appear by specification, and transient traits never appear
"""

# support
import pyre


# a protocol
class Thing(pyre.protocol, family="recipe.things"):
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
class Part(pyre.component, family="recipe.things.part", implements=Thing):
    """
    A part
    """

    level = pyre.properties.int(default=1)
    label = pyre.properties.str(default="part")


# a shared component
class Shared(pyre.component, family="recipe.things.shared", implements=Thing):
    """
    A shared thing
    """

    level = pyre.properties.int(default=0)


# the owner
class Owner(pyre.component, family="recipe.owner"):
    """
    An owner
    """

    label = pyre.properties.str(default="owner")
    weight = pyre.properties.float(default=1.0)
    count = pyre.properties.int(default=0)
    vertices = pyre.properties.list(schema=pyre.properties.tuple(schema=pyre.properties.float()))
    vertices.default = []
    home = pyre.properties.path(default="/tmp")
    site = pyre.properties.uri(default="file:/tmp")
    part = Thing()
    friend = Thing()
    friend.default = None
    derived = pyre.properties.list(schema=pyre.properties.str())
    derived.default = []
    derived.persistent = False


def test():
    # load the configuration
    pyre.loadConfiguration("recipe.yaml")
    # a shared thing, configured at construction
    shared = Shared(name="recipe.shared", level=3)
    # the owner, partly configured from the file, partly at construction
    owner = Owner(name="recipe.owner", count=4, home="/var/tmp", friend=shared)
    # runtime state
    owner.derived = ["a", "b"]
    # build the recipe
    recipe = pyre.config.newRecipe().add(owner)
    # the owner's section
    section = recipe.section("recipe.owner")
    # what came from the file
    assert section["label"] == "configured"
    assert section["weight"] == 2.5
    # containers hold the persistable form of their items, the one the loader reads back
    assert section["vertices"] == ["(1.0, 2.0)", "(3.0, 4.0)"]
    # what came from the construction
    assert section["count"] == 4
    assert section["home"] == "/var/tmp"
    # the shared component, by specification
    assert section["friend"] == "recipe.things.shared#recipe.shared"
    # the defaults are absent
    assert "site" not in section
    # the part was bound by default, so the binding is not recorded
    assert "part" not in section
    # and the transient state is absent
    assert "derived" not in section
    # the part has its own section, with what the file configured
    assert recipe.section("recipe.owner.part") == {"level": 7}
    # so does the shared component
    assert recipe.section("recipe.shared") == {"level": 3}
    # the sections come in the order the components were met
    assert list(recipe.sections) == ["recipe.owner", "recipe.owner.part", "recipe.shared"]
    # and the specifications are known
    assert recipe.spec("recipe.shared") == "recipe.things.shared#recipe.shared"
    # all done
    return recipe


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
