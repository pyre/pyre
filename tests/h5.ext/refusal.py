#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Check that a refusal by the library reaches the caller as one journal entry that says
    what was attempted and what the library had to say about it, that a fatal channel turns
    it into an exception while a quiet one hands back an empty handle, and that the library's
    own print of its error stack stays off stderr
    """
    # get the bindings
    from pyre.extensions import libh5

    # and the journal
    import journal

    # for the scratch files and the capture of stderr
    import os
    import tempfile

    # a scratch file
    uri = "h5_ext_refusal.h5"
    # make it
    f = libh5.File(uri=uri, mode="w")
    # the library will not make a group whose parent does not exist; capture stderr while it
    # refuses, to check that the library says nothing there on its own
    capture = tempfile.TemporaryFile(mode="w+b")
    saved = os.dup(2)
    os.dup2(capture.fileno(), 2)
    # attempt to make the group
    try:
        # which is refused
        f.create(path="missing/group")
    # the refusal is an error, and errors are fatal by default
    except journal.ApplicationError as error:
        # restore stderr before anything else can go wrong
        os.dup2(saved, 2)
        # the exception names the channel of the area that was asked
        assert str(error).startswith("pyre.h5.group")
    # anything else is a failure
    else:
        os.dup2(saved, 2)
        assert False, "a group with no parent was created"
    # the library printed nothing on its own
    capture.seek(0)
    assert capture.read() == b""
    # done with the capture
    os.close(saved)
    capture.close()

    # a channel that is not fatal records the entry instead; send it to a file
    log = "h5_ext_refusal.log"
    channel = journal.error("pyre.h5.group")
    channel.device = journal.file(path=log)
    channel.fatal = False
    # so the same request
    group = f.create(path="missing/group")
    # answers with a handle the library will not vouch for
    assert not libh5.valid(group.hid)
    # and the entry says what was attempted
    text = open(log, encoding="utf-8").read()
    assert "creating the group 'missing/group'" in text
    # that the library refused
    assert "the hdf5 library refused" in text
    # and what it said, which names one of its group routines
    assert "H5G" in text

    # a dataset refusal carries the dataset's name in the attempt and the library's reason
    # alongside; a closed dataset is asked for its creation property list
    dataset = f.create(
        path="data", type=libh5.types.native.double, space=libh5.DataSpace(shape=[4, 4])
    )
    dataset.close()
    # quietly
    channel = journal.error("pyre.h5.dataset")
    channel.device = journal.file(path=log)
    channel.fatal = False
    # the answer is a list the library will not vouch for
    assert not libh5.valid(dataset.dcpl.hid)
    # and the entry says what was attempted, and what the library said, which names the
    # routine that would not take the dead handle
    text = open(log, encoding="utf-8").read()
    assert "retrieving the creation property list of" in text
    assert "H5" in text.split("the hdf5 library refused")[-1]

    # clean up
    f.close()
    os.remove(uri)
    os.remove(log)
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
