#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a backup server writes a prepared statement anew at every run, with the values of the
run as literals
"""


def test():
    """
    Prepare a selection of the words of a language, and run it for two languages
    """
    # access the package
    import pyre.db

    # a table of words
    class Word(pyre.db.table, id="words"):
        """
        Words
        """

        # the word
        text = pyre.db.str()
        # and its language
        language = pyre.db.str()

    # the words of the language that is given when the statement runs
    class Language(pyre.db.query, word=Word):
        """
        The words of one language
        """

        # the word
        text = word.text
        # the restriction
        where = word.language == pyre.db.parameter(name="language", schema=pyre.db.str())

    # the file the statements go to, named after this driver and kept for inspection
    path = "backup_prepare.sql"
    # make a server that writes there
    db = pyre.db.backup(name="backup_prepare", stream=path)
    # prepare the selection
    words = db.prepareSelect(query=Language)
    # run it for one language; a backup only writes, so there are no rows
    assert list(words.run(language="greek")) == []
    # and for another
    assert list(words.run(language="latin")) == []
    # make sure everything is on disk
    db.stream.close()
    # read what was written
    with open(path) as stream:
        # all of it
        statements = stream.read()
    # two selections
    assert statements.count("SELECT") == 2, statements
    # one for each language, in order, with its value as a literal
    assert 0 <= statements.index("'greek'") < statements.index("'latin'"), statements
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
