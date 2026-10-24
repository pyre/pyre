#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a recipe says what was configured and nothing else: properties set in a file or
at construction appear as plain values, defaults are left out, owned parts appear by family
and get their own sections, shared components appear by specification, and transient traits
never appear
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

    # a number
    level = pyre.properties.int(default=1)
    # and some text
    label = pyre.properties.str(default="part")


# a shared component
class Shared(pyre.component, family="recipe.things.shared", implements=Thing):
    """
    A shared thing
    """

    # a number
    level = pyre.properties.int(default=0)


# the owner
class Owner(pyre.component, family="recipe.owner"):
    """
    An owner
    """

    # some text
    label = pyre.properties.str(default="owner")
    # a float
    weight = pyre.properties.float(default=1.0)
    # an integer
    count = pyre.properties.int(default=0)
    # a list of tuples
    vertices = pyre.properties.list(schema=pyre.properties.tuple(schema=pyre.properties.float()))
    # that starts empty
    vertices.default = []
    # a path
    home = pyre.properties.path(default="/tmp")
    # a uri
    site = pyre.properties.uri(default="file:/tmp")
    # a component bound by default
    part = Thing()
    # and one that is not
    friend = Thing()
    # since it starts out empty
    friend.default = None
    # runtime state
    derived = pyre.properties.list(schema=pyre.properties.str())
    # that starts empty
    derived.default = []
    # and that is not part of the configuration
    derived.persistent = False


def test():
    # load the configuration
    pyre.loadConfiguration("recipe.yaml")
    # a shared thing, configured at construction
    shared = Shared(name="recipe.shared", level=3)
    # the owner, partly configured from the file, partly at construction
    owner = Owner(name="recipe.keeper", count=4, home="/var/tmp", friend=shared)
    # runtime state
    owner.derived = ["a", "b"]
    # build the recipe
    recipe = pyre.config.newRecipe().add(owner)
    # the owner's section
    section = recipe.section("recipe.keeper")
    # what came from the file: the text
    assert section["label"] == "configured"
    # and the float
    assert section["weight"] == 2.5
    # containers hold their items as their schemata render them, numbers as numbers, which the
    # loader reads back
    assert section["vertices"] == [[1.0, 2.0], [3.0, 4.0]]
    # what came from the construction: the integer
    assert section["count"] == 4
    # and the path
    assert section["home"] == "/var/tmp"
    # the shared component, by specification
    assert section["friend"] == "recipe.things.shared#recipe.shared"
    # the defaults are absent
    assert "site" not in section
    # the part was bound by default; the binding is recorded anyway, by family, since it
    # decides what the section of the part means
    assert section["part"] == "recipe.things.part"
    # and the transient state is absent
    assert "derived" not in section
    # the part has its own section, with what the file configured
    assert recipe.section("recipe.keeper.part") == {"level": 7}
    # so does the shared component
    assert recipe.section("recipe.shared") == {"level": 3}
    # the sections come in the order the components were met
    assert list(recipe.sections) == ["recipe.keeper", "recipe.keeper.part", "recipe.shared"]
    # and the specifications are known
    assert recipe.spec("recipe.shared") == "recipe.things.shared#recipe.shared"
    # all done
    return recipe


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
