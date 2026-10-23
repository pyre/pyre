#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
The configuration files the executive guesses at and does not find go to a pile of their own;
a guess that is there but cannot be read, and a file named explicitly that is not there, are
errors
"""


def test() -> None:
    """
    Boot, search for and load configuration files, and check which pile each failure lands in
    """
    # support
    import os
    import shutil
    import journal
    import pyre

    # get the executive
    executive = pyre.executive
    # make a channel for what goes wrong; it fires once all the checks are done
    channel = journal.firewall("pyre.tests.framework.guesses")
    # the files i load on purpose fail, and the executive says so; the checks below read its
    # pile of errors, so its warnings are not needed on the screen
    journal.warning("pyre.configuration").device = journal.trash()

    # booting searched for configuration files, and missed most of them
    if not executive.guesses:
        # so there should be some
        channel.line("booting left no missed guesses behind")
        channel.indent()
        channel.line("look in: framework/Executive.py, Executive.configureStem")
        channel.outdent()
    # each of them must be a source that is not there
    for guess in executive.guesses:
        # if it isn't
        if not isinstance(guess, executive.fileserver.SourceNotFoundError):
            # say so
            channel.line(f"a guess failed for another reason: {type(guess).__name__}: {guess}")
    # and none of them may be among the errors
    for error in executive.errors:
        # if one is
        if isinstance(error, executive.fileserver.SourceNotFoundError):
            # say so
            channel.line(f"a missed guess is among the errors: {error}")

    # load a file that is not there, by name
    executive.loadConfiguration(uri="executive_guesses.missing.cfg")
    # it must be the last error
    if not executive.errors or "executive_guesses.missing.cfg" not in str(executive.errors[-1]):
        # if not, say so
        channel.line("a missing file named explicitly is not among the errors")
        channel.indent()
        channel.line("look in: framework/Executive.py, Executive.loadConfiguration")
        channel.outdent()

    # make a folder where a guess will look for a file, under a scratch folder named after me
    scratch = "executive_guesses.scratch"
    # start clean
    shutil.rmtree(scratch, ignore_errors=True)
    # make it, with a folder by the name of a {cfg} file inside
    os.makedirs(os.path.join(scratch, "guess.cfg"))
    # count the piles
    guesses, errors = len(executive.guesses), len(executive.errors)
    # search for configuration files named {guess} in it
    executive.configureStem(stem="guess", cfgpath=[scratch], locator=pyre.tracking.here(level=0))
    # the folder must be an error
    found = executive.errors[errors:]
    # exactly one
    if len(found) != 1 or not isinstance(found[0], executive.fileserver.IsFolderError):
        # if not, say so
        channel.line("a guess that is a folder is not exactly one error")
        channel.indent()
        channel.line(f"errors: {[str(error) for error in found]}")
        channel.line("look in: framework/Executive.py, Executive.configureStem")
        channel.outdent()
    # and the other encodings must be missed guesses
    missed = len(executive.guesses) - guesses
    # one for each encoding but {cfg}
    if missed != len(executive.configurator.encodings()) - 1:
        # if not, say so
        channel.line(f"the search missed {missed} guesses")
        channel.indent()
        channel.line(
            f"expected: one for each of {list(executive.configurator.encodings())}, but cfg"
        )
        channel.outdent()
    # clean up
    shutil.rmtree(scratch)

    # if anything went wrong
    if channel.page:
        # complain
        channel.log()

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
