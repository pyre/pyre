#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Structural check: every registered package category publishes well formed recipes
"""


def test():
    """
    Walk the category registry and validate the recipe declarations
    """
    # externals
    import re

    # support
    import pyre.externals

    # get the index class
    from pyre.externals.Index import Index

    # make an index; no engines are consulted here, so this is safe on any host
    index = Index()
    # go through the registered categories
    for category in index._categories:
        # resolve the protocol
        protocol = index.protocol(category=category)
        # it must exist
        assert protocol is not None, f"unknown category '{category}'"
        # and carry the matching category tag
        assert protocol.category == category, f"category mismatch for '{category}'"
        # collect its recipes
        recipes = tuple(protocol.recipes())
        # there must be at least one flavor
        assert recipes, f"no recipes for '{category}'"
        # go through them
        for recipe in recipes:
            # the recipe must belong to the category
            assert recipe.category == category, f"stray recipe in '{category}'"
            # the factory must implement the protocol
            assert (
                protocol in recipe.factory.pyre_implements.mro()
            ), f"factory '{recipe.factory}' does not implement '{category}'"
            # the marker patterns must be valid regular expressions
            for pattern in recipe.libraries:
                # by compiling each one
                re.compile(pattern)
            # same for the executable markers
            for pattern in recipe.binaries.values():
                # compile
                re.compile(pattern)
            # the native names must be tuples of strings
            for names in recipe.natives.values():
                # check the container
                assert isinstance(names, tuple), f"non-tuple natives in '{category}'"
            # the candidate generator must end with the category name
            assert tuple(recipe.candidates(manager="no-such-manager"))[-1] == category

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
