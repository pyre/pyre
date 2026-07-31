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
    # the pile of geometry problems, collected across all categories and reported together
    problems = []
    # go through the supported categories
    for category in index.categories():
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
            # the native names must be tuples of strings or of (lead, *companions) groups
            for names in recipe.natives.values():
                # check the container
                assert isinstance(names, tuple), f"non-tuple natives in '{category}'"
            # the candidates are (lead, companions) groups
            candidates = tuple(recipe.candidates(manager="no-such-manager"))
            # whose leads and companions are all strings
            for lead, companions in candidates:
                # check the lead
                assert isinstance(lead, str), f"non-string lead in '{category}'"
                # and each companion
                assert all(isinstance(c, str) for c in companions)
            # and the fallback lead is always the category name
            assert candidates[-1][0] == category
            # every piece of information the recipe promises must have a resting place on
            # the factory; collect the factory traits
            traits = {trait.name for trait in recipe.factory.pyre_configurables()}
            # the traits the content extractors deposit into
            harvests = tuple(proof.harvest for proof in recipe.proofs if proof.harvest)
            # the geometry each recipe section deposits into
            geometry = [
                (recipe.headers, ("incdir",)),
                (recipe.libraries, ("libdir", "libraries")),
                (recipe.binaries, ("bindir",) + tuple(recipe.binaries)),
                (recipe.defines, ("defines",)),
                (recipe.dependencies, ("dependencies",)),
                (harvests, harvests),
            ]
            # go through the sections
            for section, homes in geometry:
                # skip the empty ones
                if not section:
                    # nothing to deposit, nothing to check
                    continue
                # collect the missing resting places
                for home in homes:
                    # anything the factory doesn't declare
                    if home not in traits:
                        # is a problem
                        problems.append(f"'{recipe}': no home for '{home}'")

    # report everything at once, so a mistake doesn't set up a hunting loop
    assert not problems, "\n".join(problems)

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
