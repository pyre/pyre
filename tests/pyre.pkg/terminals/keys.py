#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    The {pyre.terminals.keys} decoder turns raw byte sequences into logical keypresses
    """
    # get the decoder
    from pyre.terminals import keys

    # a helper that feeds a byte sequence one byte at a time, reporting {None} at the end
    def feed(data):
        # a buffer over the given bytes
        buf = bytearray(data)
        # a puller that walks it, serving both the blocking and the non-blocking reads
        pull = lambda: buf.pop(0) if buf else None
        # decode a single keypress from it
        return keys.decode(pull, pull)

    # the four arrow escapes decode to their names
    assert feed(b"\x1b[A").name == keys.UP
    assert feed(b"\x1b[B").name == keys.DOWN
    assert feed(b"\x1b[C").name == keys.RIGHT
    assert feed(b"\x1b[D").name == keys.LEFT
    # the {ESC O} application-cursor variant decodes too
    assert feed(b"\x1bOA").name == keys.UP
    # the forward-delete key arrives as {ESC [ 3 ~}
    assert feed(b"\x1b[3~").name == keys.DELETE
    # a lone escape stands on its own
    assert feed(b"\x1b").name == keys.ESCAPE

    # both line terminators mean "accept"
    assert feed(b"\r").name == keys.ENTER
    assert feed(b"\n").name == keys.ENTER
    # tab, backspace (both the {8} and {127} spellings), interrupt, and space each get a name
    assert feed(b"\t").name == keys.TAB
    assert feed(b"\x08").name == keys.BACKSPACE
    assert feed(b"\x7f").name == keys.BACKSPACE
    assert feed(b"\x03").name == keys.INTERRUPT
    assert feed(b" ").name == keys.SPACE
    # a run-of-the-mill printable character comes through as itself
    a = feed(b"a")
    assert a.name == keys.CHAR and a.char == "a"
    # an exhausted stream reports end-of-input
    assert feed(b"").name == keys.EOF

    # a two-byte utf-8 character decodes to a SINGLE logical key carrying one {str} character,
    # so a caller's character count — and any backspace over it — stays correct
    accented = feed(b"\xc3\xa9")
    assert accented.name == keys.CHAR
    assert accented.char == "é"
    assert len(accented.char) == 1
    # a four-byte character likewise collapses to one {str} character
    rocket = feed(b"\xf0\x9f\x9a\x80")
    assert rocket.name == keys.CHAR
    assert rocket.char == "🚀"
    assert len(rocket.char) == 1

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
