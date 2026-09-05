#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    The C++ courier writes records the Python decoder reads back intact, awkward text included
    """
    # externals
    import os

    # the bindings
    from journal import libjournal

    # and the decoder
    import journal

    # make a pipe
    reader, writer = os.pipe()
    # a mirror
    mirror = libjournal.Trash()
    # a C++ courier on the write end, delivering to the mirror as well
    courier = libjournal.Courier(descriptor=writer, mirror=mirror)
    # check its name
    assert courier.name == "courier"
    # and its initial state
    assert courier.descriptor == writer
    assert courier.seq == 0
    assert courier.shipped == 0
    assert courier.dropped == 0
    assert not courier.dead

    # make it the default device
    libjournal.Chronicler.device = courier
    # and check the assignment sticks
    assert libjournal.Chronicler.device is courier

    # log an entry with awkward text in its page and its notes
    channel = libjournal.Informational("test.courier.cxx")
    channel.line('quote " backslash \\ tab \t greek αβγ')
    channel.log("second", multi="a\nb", odd="\x01\x1f")
    # and one on a developer channel
    debug = libjournal.Debug("test.courier.cxx")
    debug.active = True
    debug.log("whisper")

    # both went out
    assert courier.seq == 2
    assert courier.shipped == 2
    assert courier.dropped == 0
    # read them back
    lines = os.read(reader, 64 * 1024).splitlines(keepends=True)
    assert len(lines) == 2
    # decode them with the python side
    first, second = (journal.record.decode(line) for line in lines)

    # the first
    assert first.sink == "alert"
    assert first.seq == 1
    assert first.pid == os.getpid()
    assert first.time > 0
    assert first.page == ['quote " backslash \\ tab \t greek αβγ', "second"]
    assert first.channel == "test.courier.cxx"
    assert first.severity == "info"
    assert first.notes["multi"] == "a\nb"
    assert first.notes["odd"] == "\x01\x1f"
    assert first.notes["filename"].endswith("courier_cxx.py")
    # the second
    assert second.sink == "memo"
    assert second.seq == 2
    assert second.page == ["whisper"]
    assert second.severity == "debug"

    # take the far end away
    os.close(reader)
    # logging must not raise
    channel.log("absent")
    # the courier noticed
    assert courier.dead
    assert courier.shipped == 2
    # closing is harmless
    courier.close()

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
