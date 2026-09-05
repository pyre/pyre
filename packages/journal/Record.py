# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import json

# the local exceptions
from .exceptions import RecordError


# the wire form of a journal entry
class Record:
    """
    A journal entry in transit: its page and its notes

    Everything a consumer needs to know about the entry is in the notes, where the journal
    already keeps the channel, the severity, and the location, and where a courier adds the
    process, the sequence number, the time, and the host. Records travel as one JSON object
    per line, so a consumer in any language can split, parse, and forward them without
    understanding them
    """

    # constants
    # the format version; bump when the shape of the wire form changes
    version = 1
    # the names of the fields on the wire, in the order they are written
    fields = ("journal", "page", "notes")
    # the device method each severity is delivered to
    sinks = {
        "debug": "memo",
        "firewall": "memo",
        "info": "alert",
        "warning": "alert",
        "error": "alert",
        "help": "help",
    }
    # the notes a courier stamps on every record it ships; a call site that uses these names
    # for notes of its own gets them overwritten at delivery
    origin = ("pid", "seq", "time", "host")

    # public data
    page = None  # the lines of the entry
    notes = None  # the metadata of the entry

    # accessors for the identifying notes
    @property
    def severity(self):
        """
        The severity of the channel that produced the entry
        """
        # it is in the notes, where the channel put it
        return self.notes.get("severity")

    @property
    def channel(self):
        """
        The name of the channel that produced the entry
        """
        # it is in the notes, where the channel put it
        return self.notes.get("channel")

    @property
    def sink(self):
        """
        The device method the entry is delivered to, or nothing if the severity is unknown
        """
        # a function of the severity
        return self.sinks.get(self.severity)

    # factories
    @classmethod
    def stamp(cls, entry, **origin):
        """
        Build a record from a live {entry}, with the {origin} stamped into its notes

        The origin is whatever the caller knows that the journal does not, e.g. the process
        and the time; every value is stored as a string, since notes are text
        """
        # copy the page, so the record survives the entry it was drawn from
        page = [str(line) for line in entry.page]
        # and the notes; they may arrive as a native dictionary or as a bound container
        notes = {str(key): str(value) for key, value in dict(entry.notes).items()}
        # stamp the origin
        notes.update((key, str(value)) for key, value in origin.items())
        # build the record
        return cls(page=page, notes=notes)

    @classmethod
    def decode(cls, line):
        """
        Reconstruct a record from its wire form
        """
        # accept bytes as well as text
        if isinstance(line, (bytes, bytearray)):
            # attempt to
            try:
                # decode them
                line = line.decode("utf-8")
            # if they are not utf-8
            except UnicodeDecodeError as error:
                # complain
                raise RecordError(reason=f"not utf-8: {error}") from error
        # attempt to
        try:
            # parse the line
            raw = json.loads(line)
        # if it is not json
        except ValueError as error:
            # complain
            raise RecordError(reason=f"not json: {error}") from error
        # the wire form is an object
        if not isinstance(raw, dict):
            # anything else is a mistake
            raise RecordError(reason=f"not an object: '{line.strip()}'")
        # every field must be present
        missing = [field for field in cls.fields if field not in raw]
        # if any are not
        if missing:
            # complain
            raise RecordError(reason=f"missing fields: {', '.join(missing)}")
        # the version must be one this reader understands
        if raw["journal"] != cls.version:
            # complain
            raise RecordError(reason=f"unsupported version: {raw['journal']}")
        # the page is a list of strings
        page = raw["page"]
        # check it
        if not isinstance(page, list) or not all(isinstance(line, str) for line in page):
            # complain
            raise RecordError(reason="the page is not a list of strings")
        # the notes are a string to string map
        notes = raw["notes"]
        # check them
        if not isinstance(notes, dict) or not all(
            isinstance(key, str) and isinstance(value, str) for key, value in notes.items()
        ):
            # complain
            raise RecordError(reason="the notes are not a map of strings")
        # build the record
        return cls(page=page, notes=notes)

    # interface
    def raw(self):
        """
        Assemble the object that represents me on the wire, in the order the fields are declared

        Consumers that batch records render a list of these rather than concatenating lines
        """
        # easy enough
        return {"journal": self.version, "page": self.page, "notes": self.notes}

    def encode(self):
        """
        Render the record in its wire form: one line of JSON, newline terminated
        """
        # render my object compactly, keeping non-ascii text as is, and terminate the line
        return (
            json.dumps(self.raw(), ensure_ascii=False, separators=(",", ":")).encode("utf-8")
            + b"\n"
        )

    # metamethods
    def __init__(self, page, notes, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the content
        self.page = page
        self.notes = notes
        # all done
        return

    def __iter__(self):
        """
        Support for quick unpacking
        """
        # first the page
        yield self.page
        # then the notes
        yield self.notes
        # all done
        return


# end of file
