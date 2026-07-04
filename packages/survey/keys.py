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
        super().__init__(**kwds)
        # what kind of key this is; one of the module-level names
        self.name = name
        # the character it carries, set only when {name} is {CHAR} or {SPACE}
        self.char = char

    def __repr__(self):
        return f"Key({self.name!r}, {self.char!r})"


def decode(nextbyte, pending):
    """
    Read one logical keypress; {nextbyte} blocks for the next byte (or {None} at end of input),
    {pending} returns an already-available byte without blocking (or {None} when none is waiting)
    """
    # pull the first byte; its absence means the input has run dry
    lead = nextbyte()
    if lead is None:
        return Key(EOF)
    # the ordinary line terminators both mean "accept"
    if lead in (10, 13):
        return Key(ENTER)
    # a tab is its own thing, since lists often use it to advance
    if lead == 9:
        return Key(TAB)
    # both the backspace and the delete byte mean "erase the last character"
    if lead in (8, 127):
        return Key(BACKSPACE)
    # ctrl-c arrives as a raw byte in this mode, so surface it as an interrupt
    if lead == 3:
        return Key(INTERRUPT)
    # an escape either stands alone or opens a control sequence
    if lead == 27:
        return _escape(pending)
    # a space is worth naming so filters can treat it deliberately
    if lead == 32:
        return Key(SPACE, " ")
    # any other control byte is one we do not act on
    if lead < 32:
        return Key(CONTROL)
    # everything else is printable text, possibly the lead of a utf-8 sequence
    return Key(CHAR, _utf8(lead, pending))


def _escape(pending):
    """
    Interpret the bytes following an {ESC}; a bare escape when nothing sensible follows
    """
    # a lone escape has no bytes waiting behind it
    following = pending()
    if following is None:
        return Key(ESCAPE)
    # arrow and edit keys arrive as {ESC [ ...} or {ESC O ...}
    if following in (91, 79):
        # the final byte selects the actual key
        final = pending()
        arrows = {65: UP, 66: DOWN, 67: RIGHT, 68: LEFT}
        if final in arrows:
            return Key(arrows[final])
        # the forward-delete key is {ESC [ 3 ~}, so swallow its trailing tilde
        if final == 51:
            pending()
            return Key(DELETE)
        # any other sequence is one we do not model, so treat the escape as bare
        return Key(ESCAPE)
    # an escape followed by anything else is still just an escape to us
    return Key(ESCAPE)


def _utf8(lead, pending):
    """
    Assemble a full utf-8 character from its {lead} byte and any continuation bytes
    """
    # a lead below the high bit is plain ascii and stands alone
    if lead < 0x80:
        return chr(lead)
    # the top bits of the lead byte announce how many continuation bytes follow
    if lead >= 0xF0:
        count = 3
    elif lead >= 0xE0:
        count = 2
    elif lead >= 0xC0:
        count = 1
    else:
        # a stray continuation byte with no lead; hand it back as-is
        return chr(lead)
    # gather the continuation bytes that are actually waiting
    trailing = bytes(
        byte for byte in (pending() for _ in range(count)) if byte is not None
    )
    # decode the whole thing, falling back to the raw lead if it does not cohere
    try:
        return (bytes([lead]) + trailing).decode("utf-8")
    except UnicodeDecodeError:
        return chr(lead)


# end of file
