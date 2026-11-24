#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that every word a dialect reserves is spelled in visible characters

The lists of reserved words are copied from the tables of key words in the documentation of each
database. Those tables are web pages, and the page of postgres puts a zero-width space after each
underscore of a long word, so that a browser may break it across lines. The space is invisible,
and a copy of the page carries it along; this is how three words of the list of standard SQL,
array_max_cardinality, current_default_transform_group and current_transform_group_for_type,
came to hold them. A word that holds one matches no name, so a name spelled like it goes out
unquoted. The reserved words are spelled in printable ASCII: letters, digits, underscores and,
in end-exec, a hyphen. So any character outside of it is a stray
"""


def test():
    """
    Check that the reserved words of each dialect hold nothing but printable ASCII
    """
    # access the package
    import pyre.db

    # the mills of the dialects
    mills = (
        pyre.db.backends.standard.mill(name="standard"),
        pyre.db.backends.postgres.mill(name="postgres"),
        pyre.db.backends.sqlite.mill(name="sqlite"),
    )
    # go through them
    for mill in mills:
        # find the words with characters outside printable ASCII, spelled so their strays show
        strays = sorted(
            ascii(word) for word in mill.reserved if not (word.isascii() and word.isprintable())
        )
        # there should be none
        assert not strays, f"{mill.dialect}: {', '.join(strays)}"
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
