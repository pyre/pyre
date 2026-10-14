#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a recipe records lists and dicts of components by the specifications of the
components they hold, describes each of those components in its own section, and leaves out
the ones that can't be rebuilt; and that loading what it wrote rebuilds the containers
"""

# support
import pyre


# a protocol for the parts
class Part(pyre.protocol, family="recipe.containers.parts"):
    """
    Parts
    """


# a part
class Gear(pyre.component, family="recipe.containers.parts.gear", implements=Part):
    """
    A gear
    """

    # a setting
    teeth = pyre.properties.int(default=12)


# a component with containers of parts
class Machine(pyre.component, family="recipe.containers.machine"):
    """
    A machine with a list and a dict of parts
    """

    # the containers
    train = pyre.properties.list(schema=Part())
    spares = pyre.properties.dict(schema=Part())


def test():
    """
    Persist a machine and build another one out of what was written
    """
    # support
    from pyre.config.yaml import editor

    # if the backend is not available
    if not editor.available():
        # there is nothing to check
        return None

    # the file with the state; it does not exist yet
    uri = pyre.primitives.path("recipe_containers.yaml")
    # make sure
    if uri.exists():
        # by removing leftovers from an earlier run
        uri.unlink()

    # make some named parts, configured
    first = Gear(name="recipe.containers.first", teeth=20)
    second = Gear(name="recipe.containers.second", teeth=30)
    spare = Gear(name="recipe.containers.spare", teeth=40)
    # build a machine
    machine = Machine(name="recipe.containers.machine")
    # with a list of parts, one of them anonymous, which can't be rebuilt
    machine.train = [first, Gear(), second]
    # and a dict of them
    machine.spares = {"spare": spare}

    # build the recipe
    recipe = pyre.config.newRecipe().add(machine)
    # the section of the machine
    section = recipe.section("recipe.containers.machine")
    # names the components in the list by their specifications, leaving out the anonymous one
    assert section["train"] == [
        "recipe.containers.parts.gear#recipe.containers.first",
        "recipe.containers.parts.gear#recipe.containers.second",
    ], section["train"]
    # and does the same for the dict, keeping its keys
    assert section["spares"] == {"spare": "recipe.containers.parts.gear#recipe.containers.spare"}
    # each named part has a section of its own, with its settings
    assert recipe.section("recipe.containers.first") == {"teeth": 20}
    assert recipe.section("recipe.containers.second") == {"teeth": 30}
    assert recipe.section("recipe.containers.spare") == {"teeth": 40}

    # persist the machine
    machine.pyre_persist(uri=uri)
    # the file holds the specifications, not the string form of the components
    doc = pyre.config.newYamlEditor(uri=uri)
    assert list(doc.get("recipe.containers.machine", "train")) == section["train"]
    # a second machine, configured by what the first one wrote
    doc.set("recipe.containers.copy", value=doc.get("recipe.containers.machine"))
    doc.save()
    # restoring is plain configuration
    pyre.loadConfiguration(str(uri))
    # build the copy
    copy = Machine(name="recipe.containers.copy")
    # its list holds the same parts
    assert list(copy.train) == [first, second]
    # and so does its dict
    assert dict(copy.spares) == {"spare": spare}

    # all done
    return machine


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
