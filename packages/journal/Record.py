# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import json
import os
import time

# the local exceptions
from .exceptions import RecordError


# the wire form of a journal entry
class Record:
    """
    A journal entry in transit: its page and notes, the sink it was delivered to, and an
    envelope that says which process produced it and when

    Records travel as one JSON object per line, so a consumer in any language can split,
    parse, and forward them without understanding them
    """

    # constants
    # the format version; bump when the shape of the wire form changes
    version = 1
    # the sinks an entry can be delivered to
    sinks = ("alert", "memo", "help")
    # the names of the fields on the wire, in the order they are written
    fields = ("journal", "seq", "pid", "time", "sink", "page", "notes")

    # public data
    seq = 0  # the sequence number of the record within its process
    pid = 0  # the process that produced the entry
    time = 0.0  # seconds since the epoch at the flush
    sink = None  # the device method the entry was delivered to
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

    # factories
    @classmethod
    def stamp(cls, entry, sink, seq):
        """
        Build a record from a live {entry} bound for {sink}, stamped with the current
        process id and time
        """
        # copy the page, so the record survives the entry it was drawn from
        page = [str(line) for line in entry.page]
        # and the notes; they may arrive as a native dictionary or as a bound container
        notes = {str(key): str(value) for key, value in dict(entry.notes).items()}
        # build the record
        return cls(sink=sink, page=page, notes=notes, seq=seq, pid=os.getpid(), time=time.time())

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
        # the sink must be one of the three
        if raw["sink"] not in cls.sinks:
            # complain
            raise RecordError(reason=f"unknown sink: '{raw['sink']}'")
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
        # the envelope is numeric
        try:
            # coerce each field
            seq = int(raw["seq"])
            pid = int(raw["pid"])
            stamp = float(raw["time"])
        # if any of them isn't
        except (TypeError, ValueError) as error:
            # complain
            raise RecordError(reason=f"malformed envelope: {error}") from error
        # build the record
        return cls(sink=raw["sink"], page=page, notes=notes, seq=seq, pid=pid, time=stamp)

    # interface
    def encode(self):
        """
        Render the record in its wire form: one line of JSON, newline terminated
        """
        # assemble the object in the order the fields are declared
        raw = {
            "journal": self.version,
            "seq": self.seq,
            "pid": self.pid,
            "time": self.time,
            "sink": self.sink,
            "page": self.page,
            "notes": self.notes,
        }
        # render it compactly, keeping non-ascii text as is, and terminate the line
        return json.dumps(raw, ensure_ascii=False, separators=(",", ":")).encode("utf-8") + b"\n"

    # metamethods
    def __init__(self, sink, page, notes, seq, pid, time, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the sink
        self.sink = sink
        # the content
        self.page = page
        self.notes = notes
        # and the envelope
        self.seq = seq
        self.pid = pid
        self.time = time
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
