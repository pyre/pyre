# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Decode a raw terminal byte stream into logical keypresses
"""

# the names a decoded key can carry
UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"
ENTER = "enter"
BACKSPACE = "backspace"
DELETE = "delete"
TAB = "tab"
ESCAPE = "escape"
SPACE = "space"
INTERRUPT = "interrupt"
CONTROL = "control"
CHAR = "char"
EOF = "eof"


class Key:
    """
    A single decoded keypress: either a printable character or a named special key
    """

    def __init__(self, name, char=None, **kwds):
        # chain up
        super().__init__(**kwds)
        # remember what kind of key this is; one of the module-level names
        self.name = name
        # and the character it carries, set only when {name} is {CHAR} or {SPACE}
        self.char = char

    def __repr__(self):
        # render enough to recognize the key while debugging
        return f"Key({self.name!r}, {self.char!r})"


def decode(nextbyte, pending):
    """
    Read one logical keypress; {nextbyte} blocks for the next byte (or {None} at end of input),
    {pending} returns an already-available byte without blocking (or {None} when none is waiting)
    """
    # pull the first byte of the keypress
    lead = nextbyte()
    # nothing waiting means the input has run dry
    if lead is None:
        # so report the end
        return Key(EOF)
    # the two line terminators both mean "accept the current answer"
    if lead in (10, 13):
        # so name it the enter key
        return Key(ENTER)
    # a tab often advances the highlight in a list, so it earns its own name
    if lead == 9:
        # report it as a tab
        return Key(TAB)
    # backspace and the delete byte both mean "erase the last character"
    if lead in (8, 127):
        # collapse them into a single backspace
        return Key(BACKSPACE)
    # ctrl-c reaches us as a raw byte in this mode
    if lead == 3:
        # surface it as an interrupt so callers can bail
        return Key(INTERRUPT)
    # an escape either stands alone or opens a control sequence
    if lead == 27:
        # hand the rest of the sequence to the escape reader
        return _escape(pending)
    # a space is named so filters can treat it deliberately
    if lead == 32:
        # carry the actual character along for filtering
        return Key(SPACE, " ")
    # any other control byte is one we do not act on
    if lead < 32:
        # report it generically and move on
        return Key(CONTROL)
    # everything else is printable text, maybe the lead of a utf-8 sequence
    return Key(CHAR, _utf8(lead, pending))


def _escape(pending):
    """
    Interpret the bytes following an {ESC}; a bare escape when nothing sensible follows
    """
    # look for a byte riding behind the escape
    following = pending()
    # a lone escape has nothing waiting
    if following is None:
        # so it really was just an escape
        return Key(ESCAPE)
    # arrow and edit keys arrive as {ESC [ ...} or {ESC O ...}
    if following in (91, 79):
        # the final byte selects the actual key
        final = pending()
        # map the four arrow terminators to their names
        arrows = {65: UP, 66: DOWN, 67: RIGHT, 68: LEFT}
        # an arrow is the common case
        if final in arrows:
            # report the arrow it names
            return Key(arrows[final])
        # the forward-delete key is {ESC [ 3 ~}
        if final == 51:
            # swallow its trailing tilde
            pending()
            # and report a delete
            return Key(DELETE)
        # any other sequence is one we do not model
        return Key(ESCAPE)
    # an escape followed by anything else is still just an escape to us
    return Key(ESCAPE)


def _utf8(lead, pending):
    """
    Assemble a full utf-8 character from its {lead} byte and any continuation bytes
    """
    # a lead below the high bit is plain ascii and stands alone
    if lead < 0x80:
        # so return it directly
        return chr(lead)
    # the top bits of the lead byte announce how many continuation bytes follow
    if lead >= 0xF0:
        # a four-byte sequence has three continuations
        count = 3
    # a three-byte sequence
    elif lead >= 0xE0:
        # has two
        count = 2
    # a two-byte sequence
    elif lead >= 0xC0:
        # has one
        count = 1
    # everybody else
    else:
        # is a stray continuation byte with no lead; hand it back as-is
        return chr(lead)
    # gather the continuation bytes that are actually waiting
    trailing = bytes(byte for byte in (pending() for _ in range(count)) if byte is not None)
    # attempt to
    try:
        # decode the assembled bytes as a single character
        return (bytes([lead]) + trailing).decode("utf-8")
    # if the decoder fails
    except UnicodeDecodeError:
        # fall back to the raw lead
        return chr(lead)


# end of file
