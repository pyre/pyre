#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    A data type code that ENVI does not define is refused: a header read from a file leaves the
    code unset and keeps its text in the extras, and a header that is assigned the code refuses to
    look it up
    """
    # access the package
    import pyre
    import journal

    # for a header in memory
    import io

    # the reader warns about the refused code, so send its warnings to a file
    journal.warning("pyre.envi.header").device = journal.file(path="datatype_unknown.log")

    # a header with a code that falls in a gap of the ENVI table
    text = "ENVI\nsamples = 10\ndata type = 7\n"
    # parse it
    header = pyre.envi.reader().parse(stream=io.StringIO(text), uri="memory")
    # the good field made it
    assert header.samples == 10
    # the code did not
    assert header.dataType is None
    # so there is no cell type
    assert header.datatype is None
    # and the text of the code is in the bag
    assert header.extras == {"data type": "7"}

    # get the warnings
    with open("datatype_unknown.log") as stream:
        # all of them
        report = stream.read()
    # the header says the value is not allowed
    assert "the value of 'data type', '7', is not allowed" in report, report
    # and why, in the words of the trait
    assert "7 is not a member of {1, 2, 3, 4, 5, 6, 9, 12, 13, 14, 15}" in report, report
    # without saying where the trait lives
    assert "an instance of" not in report, report

    # a header that is assigned the same code
    header = pyre.envi.header()
    # takes it
    header.dataType = 7
    # but refuses to look it up
    try:
        # ask for the cell type
        header.datatype
        # if the lookup succeeds, the code was accepted
        assert False, "an undefined data type code was looked up"
    # the refusal
    except header.TraitValueError as error:
        # names the trait
        assert error.trait == "dataType", error.trait
        # and the value
        assert error.value == 7, error.value

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
