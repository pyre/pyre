#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a component has no suggestions for its traits by default, and that one that knows its
way around a trait can make them from its current state
"""


def test():
    # support
    import pyre

    # a component with nothing to suggest
    class plain(pyre.component):
        """a component with a trait and no suggestions"""

        # a trait
        size = pyre.properties.int()
        size.default = 4

    # one that suggests multiples of a trait for another
    class helpful(pyre.component):
        """a component that suggests values for one of its traits"""

        # the trait that drives the suggestions
        size = pyre.properties.int()
        size.default = 4
        # the trait it suggests values for
        total = pyre.properties.int()

        # the hook
        def pyre_suggest(self, trait):
            """suggest multiples of my size for my total"""
            # for anything other than my total
            if trait.name != "total":
                # defer to the framework
                yield from super().pyre_suggest(trait=trait)
                # and stop
                return
            # otherwise, suggest the first few multiples of my size
            yield from (self.size * k for k in range(1, 4))
            # all done
            return

    # make the plain one
    p = plain(name="plain")
    # it has nothing to suggest
    assert list(p.pyre_suggest(trait=plain.pyre_trait(alias="size"))) == []

    # make the helpful one
    h = helpful(name="helpful")
    # it has nothing to suggest for its size
    assert list(h.pyre_suggest(trait=helpful.pyre_trait(alias="size"))) == []
    # but it suggests multiples of its size for its total
    assert list(h.pyre_suggest(trait=helpful.pyre_trait(alias="total"))) == [4, 8, 12]
    # and the suggestions follow its state: change its size
    h.size = 5
    # and its suggestions for the total change with it
    assert list(h.pyre_suggest(trait=helpful.pyre_trait(alias="total"))) == [5, 10, 15]

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
