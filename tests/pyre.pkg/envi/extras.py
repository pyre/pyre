#! /usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    A known keyword whose value cannot be converted lands in the extras as text, with a warning,
    rather than aborting the read
    """
    # access the package
    import pyre
    import journal

    # for a header in memory
    import io

    # the warnings are expected, from the header and from the list that drops a bad item, so
    # send them to a file
    log = journal.file(path="extras.log")
    journal.warning("pyre.envi.header").device = log
    journal.warning("pyre.config.containers").device = log

    # a header with a bad line count and a bad wavelength list
    text = "\n".join(
        [
            "ENVI",
            "samples = 10",
            "lines = many",
            "wavelength = {0.4, blue, 0.6}",
            "",
        ]
    )
    # parse it
    hdr = pyre.envi.reader().parse(stream=io.StringIO(text), uri="memory")

    # the good field made it
    assert hdr.samples == 10
    # the bad ones did not
    assert hdr.lines is None
    assert hdr.wavelength is None
    # and their text is in the bag, a bare value as a string and a braced one as a list
    assert hdr.extras == {"lines": "many", "wavelength": ["0.4", "blue", "0.6"]}

    # get the warnings
    with open("extras.log") as stream:
        # all of them
        report = stream.read()
    # the list says which item it dropped, and why
    assert "skipping 'blue': could not coerce 'blue' into a float" in report, report
    # the header adds the value it read and the type it expected
    assert "the value of 'wavelength', {0.4, blue, 0.6}, is not of type 'list[float]'" in report
    # and says what became of it
    assert "so 'wavelength' is left unset; its text is in the extras of the header" in report
    # for a scalar, nobody said why, so the header passes on the reason, once
    assert report.count("could not coerce 'many' into an integer") == 1, report
    # and no message repeats what another one already said
    assert report.count("could not coerce 'blue'") == 1, report

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
