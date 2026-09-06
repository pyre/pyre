# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre
import journal

# the header
from .Header import Header

# the local exceptions
from . import exceptions


# the ENVI header reader
class Reader:
    """
    A reader of ENVI headers

    The text is a sequence of {keyword = value} entries after a line with the {ENVI} marker;
    lines that start with a semicolon are comments, and a value in braces may span lines. Known
    keywords land on the traits of the header, converted to their documented types; a known
    keyword whose value cannot be converted, and every keyword the standard does not define, land
    in the header's {extras} as text.
    """

    # constants
    # the marker that opens every header
    marker = "ENVI"
    # the comment leader
    comment = ";"

    # interface
    def read(self, uri, name: str | None = None) -> Header:
        """
        Read the header at {uri}
        """
        # the location, as a path
        path = pyre.primitives.path(uri)
        # open the file; headers are ASCII, so anything else is tolerated rather than fatal
        with open(path, mode="r", encoding="utf-8", errors="replace") as stream:
            # and parse it
            return self.parse(stream=stream, uri=str(path), name=name)

    def parse(self, stream, uri: str = "<stream>", name: str | None = None) -> Header:
        """
        Build a header out of the lines of {stream}; {uri} labels the source in complaints
        """
        # scan the text into (keyword, value) pairs
        entries = self.scan(stream=stream, uri=uri)
        # and assemble the header
        return self.assemble(entries=entries, uri=uri, name=name)

    # implementation details
    def scan(self, stream, uri: str):
        """
        Scan the lines of {stream} and generate (keyword, value) pairs; a value is a string when
        bare and a list of strings when braced
        """
        # number the lines, the way editors do
        lines = enumerate(stream, start=1)
        # the first significant line must be the marker
        for number, line in lines:
            # clean up
            text = line.strip()
            # skip blank lines and comments
            if not text or text.startswith(self.comment):
                # by moving on
                continue
            # anything else must be the marker
            if text != self.marker:
                # or this is not an ENVI header
                raise exceptions.MissingMarkerError(uri=uri)
            # found it
            break
        # if the loop ran out of lines
        else:
            # the file is empty
            raise exceptions.MissingMarkerError(uri=uri)

        # go through the rest
        for number, line in lines:
            # clean up
            text = line.strip()
            # skip blank lines and comments
            if not text or text.startswith(self.comment):
                # by moving on
                continue
            # an entry is an assignment; split on the first {=} only, since values may contain
            # more of them
            keyword, separator, value = text.partition("=")
            # if there is no separator
            if not separator:
                # the line is not an entry
                raise exceptions.MalformedHeaderError(
                    uri=uri, line=number, text=text, reason="expected 'keyword = value'"
                )
            # normalize the keyword: lower case, with single spaces
            keyword = " ".join(keyword.split()).lower()
            # and clean up the value
            value = value.strip()
            # a braced value
            if value.startswith("{"):
                # collects everything up to the closing brace, however many lines that takes
                pieces = []
                # the remainder of this line
                body = value[1:]
                # the number of the line that opened the brace, for the complaint
                opener = number
                # until the closing brace shows up
                while "}" not in body:
                    # keep this piece
                    pieces.append(body.strip())
                    # get the next line
                    try:
                        # numbered
                        number, line = next(lines)
                    # if there isn't one
                    except StopIteration:
                        # the brace was never closed
                        raise exceptions.MalformedHeaderError(
                            uri=uri, line=opener, text=text, reason="unterminated brace"
                        )
                    # this is the new body
                    body = line
                # keep the part before the closing brace
                pieces.append(body[: body.index("}")].strip())
                # the items are separated by commas; drop empty ones
                items = [item.strip() for item in " ".join(pieces).split(",")]
                # and hand off the list
                yield keyword, [item for item in items if item]
            # a bare value
            else:
                # is handed off as is
                yield keyword, value
        # all done
        return

    def assemble(self, entries, uri: str, name: str | None) -> Header:
        """
        Build a header out of (keyword, value) {entries}
        """
        # make a header; parsed values are deposited by assignment rather than as constructor
        # keywords: assignment works for anonymous headers, applies one value at a time so a bad
        # one can be diverted to the extras, and records facts about the file above any
        # configuration, which is where they belong
        header = Header(name=name)
        # make a channel for complaints about values
        channel = journal.warning("pyre.envi.header")
        # go through the entries
        for keyword, value in entries:
            # look for the trait that answers to this keyword
            try:
                # by alias
                trait = Header.pyre_trait(alias=keyword)
            # if there isn't one
            except Header.TraitNotFoundError:
                # the keyword goes in the bag as is
                header.extras[keyword] = value
                # and we are done with it
                continue
            # a braced value bound for a trait travels as text; scalar traits get the items
            # joined back with commas, which the sequence traits split again
            text = ", ".join(value) if isinstance(value, list) else value
            # attempt to
            try:
                # deposit the value
                setattr(header, trait.name, text)
                # and read it back, which is when the conversion to the documented type happens
                converted = getattr(header, trait.name)
                # a sequence trait drops the items it cannot convert rather than failing, so a
                # braced value that came back as a shorter sequence has lost something; a text
                # trait gets the whole braced value as one string, so it is not subject to this
                if (
                    isinstance(value, list)
                    and isinstance(converted, (list, tuple))
                    and len(converted) != len(value)
                ):
                    # which is a failure as well
                    raise exceptions.MalformedValueError(keyword=keyword, value=value)
            # if the conversion fails
            except pyre.PyreError as error:
                # the trait stays unset
                setattr(header, trait.name, None)
                # the value goes in the bag as text
                header.extras[keyword] = value
                # and the user hears about it
                channel.line(f"while reading '{uri}'")
                channel.indent()
                channel.line(f"could not convert the value of '{keyword}': {error}")
                channel.line(f"the text is available in the extras of the header")
                channel.outdent()
                channel.log()
        # all done
        return header


# end of file
