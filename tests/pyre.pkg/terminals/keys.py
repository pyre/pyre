#!/usr/bin/env python3
# -*- python -*-
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
        """
        Decode one keypress from {data}
        """
        # a buffer over the given bytes
        buffer = bytearray(data)
        # a puller that walks it, serving both the blocking and the non-blocking reads
        pull = lambda: buffer.pop(0) if buffer else None
        # decode a single keypress from it
        return keys.decode(pull, pull)

    # the four arrow escapes decode to their names
    assert feed(b"\x1b[A").name == keys.UP
    # down
    assert feed(b"\x1b[B").name == keys.DOWN
    # right
    assert feed(b"\x1b[C").name == keys.RIGHT
    # and left
    assert feed(b"\x1b[D").name == keys.LEFT
    # the {ESC O} application-cursor variant decodes too
    assert feed(b"\x1bOA").name == keys.UP
    # the forward-delete key arrives as {ESC [ 3 ~}
    assert feed(b"\x1b[3~").name == keys.DELETE
    # a lone escape stands on its own
    assert feed(b"\x1b").name == keys.ESCAPE

    # both line terminators mean "accept"
    assert feed(b"\r").name == keys.ENTER
    # the newline too
    assert feed(b"\n").name == keys.ENTER
    # tab, backspace (both the {8} and {127} spellings), interrupt, and space each get a name
    assert feed(b"\t").name == keys.TAB
    # backspace
    assert feed(b"\x08").name == keys.BACKSPACE
    # in both spellings
    assert feed(b"\x7f").name == keys.BACKSPACE
    # interrupt
    assert feed(b"\x03").name == keys.INTERRUPT
    # and space
    assert feed(b" ").name == keys.SPACE
    # a run-of-the-mill printable character comes through as itself
    a = feed(b"a")
    # is a character
    assert a.name == keys.CHAR
    # carrying the character
    assert a.char == "a"
    # an exhausted stream reports end-of-input
    assert feed(b"").name == keys.EOF

    # a two-byte utf-8 character decodes to a SINGLE logical key carrying one {str} character,
    # so a caller's character count — and any backspace over it — stays correct
    accented = feed(b"\xc3\xa9")
    # is a character
    assert accented.name == keys.CHAR
    # carrying the character
    assert accented.char == "é"
    # which is just one
    assert len(accented.char) == 1
    # a four-byte character likewise collapses to one {str} character
    rocket = feed(b"\xf0\x9f\x9a\x80")
    # is a character
    assert rocket.name == keys.CHAR
    # carrying the character
    assert rocket.char == "🚀"
    # which is just one
    assert len(rocket.char) == 1

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
