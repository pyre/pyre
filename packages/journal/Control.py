# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import json

# the local exceptions
from .exceptions import RecordError


# an instruction to a channel in another process
class Control:
    """
    A change to the state of a journal channel, in transit: the severity and name that identify
    the channel, and the flags to set

    Controls travel the way records do, one JSON object per line, so the far end can split and
    parse them the same way; a flag left unset is left alone when the control is applied
    """

    # constants
    # the format version; shared with records, since they travel the same wires
    version = 1
    # the marker that tells a control apart from a record
    kind = "control"
    # the flags a control can set
    flags = ("active", "fatal")

    # public data
    severity = None  # the severity of the channel
    name = None  # its name
    active = None  # whether it should speak, or unset
    fatal = None  # whether it should abort after speaking, or unset

    # factories
    @classmethod
    def decode(cls, line):
        """
        Reconstruct a control from its wire form
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
        # of the right version
        if raw.get("journal") != cls.version:
            # complain
            raise RecordError(reason=f"unsupported version: {raw.get('journal')}")
        # and the right kind
        if raw.get("kind") != cls.kind:
            # complain
            raise RecordError(reason=f"not a control: '{raw.get('kind')}'")
        # the channel identity is a pair of strings
        severity = raw.get("severity")
        name = raw.get("name")
        # check
        if not isinstance(severity, str) or not isinstance(name, str):
            # complain
            raise RecordError(reason="the channel identity is not a pair of strings")
        # the flags are booleans, or absent
        flags = {}
        # go through them
        for flag in cls.flags:
            # get the value
            value = raw.get(flag)
            # check it
            if value is not None and not isinstance(value, bool):
                # complain
                raise RecordError(reason=f"the '{flag}' flag is not a boolean")
            # save it
            flags[flag] = value
        # build the control
        return cls(severity=severity, name=name, **flags)

    # interface
    def apply(self):
        """
        Set the flags on the channel i identify, in this process
        """
        # the channel factories, by severity; imported here since the package publishes them
        # after it has chosen an implementation
        from . import severities

        # find the factory for the severity
        factory = severities.get(self.severity)
        # if there isn't one
        if factory is None:
            # the control is not one of ours
            raise RecordError(reason=f"unknown severity '{self.severity}'")
        # open the channel; the state is shared by everybody with this name
        channel = factory(self.name)
        # set the flags that were given
        if self.active is not None:
            # whether it speaks
            channel.active = self.active
        if self.fatal is not None:
            # whether it aborts after speaking
            channel.fatal = self.fatal
        # all done
        return channel

    def raw(self):
        """
        Assemble the object that represents me on the wire
        """
        # the identity, and the flags that were given
        raw = {
            "journal": self.version,
            "kind": self.kind,
            "severity": self.severity,
            "name": self.name,
        }
        # go through the flags
        for flag in self.flags:
            # get the value
            value = getattr(self, flag)
            # if it was given
            if value is not None:
                # include it
                raw[flag] = value
        # all done
        return raw

    def encode(self):
        """
        Render the control in its wire form: one line of JSON, newline terminated
        """
        # render my object compactly and terminate the line
        return json.dumps(self.raw(), separators=(",", ":")).encode("utf-8") + b"\n"

    # metamethods
    def __init__(self, severity, name, active=None, fatal=None, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the identity
        self.severity = severity
        self.name = name
        # and the flags
        self.active = active
        self.fatal = fatal
        # all done
        return


# end of file
