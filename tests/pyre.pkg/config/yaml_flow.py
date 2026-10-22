#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
The yaml reader makes a scope of a mapping in block form and a value of a mapping in flow form,
empty or not, at any depth, under a conditional key, and through an alias, which keeps the form of
its anchor
"""


def test() -> None:
    """
    Read small documents and compare the events the reader makes of them with what they mean
    """
    # externals
    import io

    # support
    from pyre.config.yaml.Parser import Parser

    def events(text):
        """
        Read {text} and describe each event it makes as a string
        """
        # make a reader
        parser = Parser()
        # read the text
        made = parser.parse(uri="yaml_flow.yaml", stream=io.StringIO(text), locator=None)
        # describe each event
        return [describe(event) for event in made]

    def describe(event):
        """
        Describe {event}: the name it sets, its value, and the component it is meant for, if any
        """
        # the name the event sets
        name = ".".join(event.key)
        # a conditional assignment names the component it is meant for
        if isinstance(event, Parser.ConditionalAssignment):
            # along with its name and value
            return f"{'.'.join(event.component)}: {name} <- {event.value!r}"
        # any other assignment is its name and value
        return f"{name} <- {event.value!r}"

    # each document, and what it must mean
    cases = [
        # an empty map in flow form is a value
        ("a: {}\n", ["a <- {}"]),
        # and so is one with entries
        ("a: {k: v}\n", ["a <- {'k': 'v'}"]),
        # while a map in block form is a scope
        ("a:\n  k: v\n", ["a.k <- 'v'"]),
        # at any depth
        ("a:\n  b: {k: v}\n  c:\n    k: w\n", ["a.b <- {'k': 'v'}", "a.c.k <- 'w'"]),
        # dots in the keys of a flow map stay in the value, rather than making levels
        ("a: {x.y: 1}\n", ["a <- {'x.y': 1}"]),
        # a flow map under a conditional key is the value of the conditional assignment
        ("fam#probe:\n  d: {k: v}\n", ["probe: d <- {'k': 'v'}"]),
        # an alias keeps the form of its anchor: a flow anchor is a value
        ("a: &m {k: v}\nb: *m\n", ["a <- {'k': 'v'}", "b <- {'k': 'v'}"]),
        # and a block anchor is a scope
        ("a: &n\n  k: v\nb: *n\n", ["a.k <- 'v'", "b.k <- 'v'"]),
    ]

    # go through them
    for text, expected in cases:
        # read the document
        made = events(text)
        # and compare
        assert made == expected, (text, made)

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
