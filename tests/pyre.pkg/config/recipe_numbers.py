#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a recipe records containers of numbers as numbers, and that loading what it wrote
rebuilds them
"""

# support
import pyre


# a component with containers of numbers
class Shape(pyre.component, family="recipe.numbers.shape"):
    """
    A shape with a list of vertices and a matrix
    """

    # the vertices
    vertices = pyre.properties.list(schema=pyre.properties.tuple(schema=pyre.properties.float()))
    # and a matrix
    matrix = pyre.properties.array(shape=(2, 2))


def test():
    """
    Persist a shape and build another one out of what was written
    """
    # support
    from pyre.config.yaml import editor

    # if the backend is not available
    if not editor.available():
        # there is nothing to check
        return None
    # the file with the state; it does not exist yet
    uri = pyre.primitives.path("recipe_numbers.yaml")
    # make sure
    if uri.exists():
        # by removing leftovers from an earlier run
        uri.unlink()
    # build a shape
    shape = Shape(name="recipe.numbers.square")
    # with some vertices
    shape.vertices = [(1.0, 2.0), (3.0, 4.0)]
    # and a matrix
    shape.matrix = [[1, 0], [0, 1]]
    # build the recipe
    recipe = pyre.config.newRecipe().add(shape)
    # the section of the shape
    section = recipe.section("recipe.numbers.square")
    # holds the vertices as numbers
    assert section["vertices"] == [[1.0, 2.0], [3.0, 4.0]], section["vertices"]
    # and so does the matrix
    assert section["matrix"] == [[1.0, 0.0], [0.0, 1.0]], section["matrix"]
    # persist the shape
    shape.pyre_persist(uri=uri)
    # a second shape, configured by what the first one wrote
    doc = pyre.config.newYamlEditor(uri=uri)
    # under a name of its own
    doc.set("recipe.numbers.copy", value=doc.get("recipe.numbers.square"))
    # saved with the rest
    doc.save()
    # restoring is plain configuration
    pyre.loadConfiguration(str(uri))
    # build the copy
    copy = Shape(name="recipe.numbers.copy")
    # its vertices are the same
    assert list(copy.vertices) == [(1.0, 2.0), (3.0, 4.0)], copy.vertices
    # and so is its matrix
    assert copy.matrix == ((1.0, 0.0), (0.0, 1.0)), copy.matrix

    # all done
    return shape


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
