# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import sys  # location information

# my metaclass
from .Severity import Severity

# the index
from .Index import Index

# the shared state
from .Inventory import Inventory

# the keeper of the global settings
from .Chronicler import Chronicler


# access to the channel shared state
class Channel(metaclass=Severity):
    """
    Encapsulation of the per-channel shared state

    All channels of a given severity that have the same name access a common state object. This
    enables a type of context-free control of a channel: anybody with access to the name of a
    channel can control whether it's active, or what device it writes to.
    """

    # types
    from .exceptions import JournalError

    # public data
    dent = 0  # default indentation level
    detail = 1  # default detail

    # my name
    @property
    def name(self):
        """
        Get my name
        """
        # easy enough
        return self._name

    # access to settings from my shared inventory
    @property
    def active(self):
        """
        Get my activation state
        """
        # ask my inventory
        return self.inventory.active

    @active.setter
    def active(self, active):
        """
        Set my activation state
        """
        # adjust my inventory
        self.inventory.active = active
        # all done
        return

    @property
    def fatal(self):
        """
        Check whether i'm fatal
        """
        # ask my inventory
        return self.inventory.fatal

    @fatal.setter
    def fatal(self, fatal):
        """
        Mark me as {fatal}
        """
        # adjust my inventory
        self.inventory.fatal = fatal
        # all done
        return

    @property
    def device(self):
        """
        Get my device
        """
        # first, look in my inventory for a local setting
        device = self.inventory.device
        # if it's set
        if device is not None:
            # that's the one
            return device
        # next, check whether there is a severity wide default registered with my index
        device = self.index.device
        # if it's set
        if device is not None:
            # that's the one
            return device
        # next, look for the global default
        device = self.chronicler.device
        # if it's set
        if device is not None:
            # that's the one
            return device
        # if all else fails, get the trash can
        from .Trash import Trash

        # make one and hand it off
        return Trash()

    @device.setter
    def device(self, device):
        """
        Set my device
        """
        # hand it to my inventory
        self.inventory.device = device
        # all done
        return

    # access to the severity wide defaults from my instances; my metaclass grants access to
    # them from the class itself
    @property
    def defaultActive(self):
        """
        The default activation state of the channels of my severity
        """
        # ask my class
        return type(self).defaultActive

    @property
    def defaultFatal(self):
        """
        The default fatality of the channels of my severity
        """
        # ask my class
        return type(self).defaultFatal

    @property
    def defaultDevice(self):
        """
        The default device of the channels of my severity
        """
        # ask my class
        return type(self).defaultDevice

    # control over the severity wide device
    @classmethod
    def getDefaultDevice(cls):
        """
        Get the default device associated with all channels of this severity
        """
        # my index has it
        return cls.index.device

    @classmethod
    def setDefaultDevice(cls, device):
        """
        Set the default device associated with all channels of this severity to {device}, and
        return the previous setting
        """
        # get the previous setting
        old = cls.index.device
        # install the new device
        cls.index.device = device
        # all done
        return old

    # convenient configuration
    @classmethod
    def quiet(cls):
        """
        Suppress output from all channels of this severity
        """
        # get the trash can
        from .Trash import Trash

        # make one
        trash = Trash()
        # and install it as the default device
        return cls.setDefaultDevice(trash)

    @classmethod
    def logfile(cls, path, mode="w"):
        """
        Send output from all channels of this severity to a log file
        """
        # get the file device
        from .File import File

        # make one
        log = File(path, mode)
        # and install it as the default
        return cls.setDefaultDevice(log)

    # access to information from my current entry
    @property
    def page(self):
        """
        Return the contents of my entry
        """
        # ask and pass on
        return self.entry.page

    @property
    def notes(self):
        """
        Return the metadata of the current message
        """
        # ask and pass on
        return self.entry.notes

    # interface
    def activate(self):
        """
        Enable the recording of messages
        """
        # easy
        self.active = True
        # all done
        return self

    def deactivate(self):
        """
        Disable the recording of messages
        """
        # easy
        self.active = False
        # all done
        return self

    def indent(self, levels=1):
        """
        Increase my indentation by {levels}
        """
        # clip from below and apply
        self.dent = max(0, self.dent + levels)
        # all done
        return self

    def outdent(self, levels=1):
        """
        Decrease my indentation by {levels}
        """
        # clip from below and apply
        self.dent = max(0, self.dent - levels)
        # all done
        return self

    def line(self, message=""):
        """
        Add {message} to the current page
        """
        # add message to my page
        self.page.append(self.chronicler.margin * self.dent + str(message))
        # all done
        return self

    def report(self, report):
        """
        Add lines from the {report} to the current page
        """
        # go through the lines in the {report}
        for entry in report:
            # and add each one at my current indentation
            self.line(entry)
        # all done
        return self

    def log(self, message=None, **kwds):
        """
        Add {message} to the current page and then record the entry
        """
        # if there is a final {message} to process
        if message is not None:
            # render it
            text = str(message)
            # an empty one adds nothing, so a bare flush records only what is already on the page
            if text:
                # add it to the page
                self.line(text)

        # get the frame of my caller, which is all the location information needs; a stack trace
        # would also read the text of the line from the source file, which is never used
        frame = sys._getframe(1)
        # get its code
        code = frame.f_code
        # and extract the location information
        filename, line, function = code.co_filename, frame.f_lineno, code.co_name

        # decorate my current metadata
        notes = self.notes
        # with location information
        notes["filename"] = filename
        notes["line"] = str(line)
        notes["function"] = function
        # and any additional arguments
        for key, value in kwds.items():
            # as notes
            notes[str(key)] = str(value)

        # fatal channels, e.g. errors and firewalls, raise exceptions as part of committing a
        # message to the journal. such exceptions may be caught and handled, and the channel
        # instance may continue to be used. this leads to text accumulating on my page, and the
        # next time i'm flushed, my {entry} still contains lines from the previous
        # message. the awkward block that follows attempts to prevent this by catching
        # exceptions, cleaning up the {entry} in the finally section, and re-raising the
        # exception. of course, if no exception is raised, we just clean up the page and move
        # on

        # ask my severity what the entry leads to, while the entry still holds the message
        outcome = self.outcome()

        # carefully
        try:
            # commit the message to the journal
            self.commit()
        # if i'm a fatal diagnostic, {commit} raises a journal exception
        except self.JournalError:
            # no worries; someone else may know what to do
            raise
        # but in any case
        finally:
            # start a fresh page; the notes carry over, since they accumulate for my lifetime
            self.entry = self.newEntry(notes=self.entry.notes)

        # hand back the outcome
        return outcome

    # metamethods
    def __init__(self, name, detail=detail, dent=dent, **kwds):
        # chain up
        super().__init__(**kwds)

        # save my name
        self._name = name
        # set my detail
        self.detail = detail
        # and my indentation level
        self.dent = dent
        # look up my inventory
        self.inventory = self.index.lookup(name)
        # start out with an empty entry
        self.entry = self.newEntry()

        # all done
        return

    @classmethod
    def initializeIndex(cls, active: bool, fatal: bool):
        """
        Build the index of the channels of my severity, with the given default state
        """
        # make one
        return Index(active=active, fatal=fatal)

    @classmethod
    def activateChannels(cls, names) -> None:
        """
        Activate the channels of my severity in {names}
        """
        # go through the names
        for name in names:
            # make a channel by this name and activate it
            cls(name).activate()
        # all done
        return

    @classmethod
    def __init_subclass__(cls, active=True, fatal=False, **kwds):
        # chain up
        super().__init_subclass__(**kwds)
        # give the severity an index of its own, with its default channel state
        cls.index = cls.initializeIndex(active=active, fatal=fatal)
        # all done
        return

    def __bool__(self):
        """
        Simplify activation state testing
        """
        return self.inventory.active

    # implementation details
    def commit(self):
        """
        Commit the accumulated message to my device and flush
        """
        # if i'm not active
        if not self.active:
            # nothing to do
            return self

        # if my detail exceeds the maximum
        if self.detail > self.chronicler.detail:
            # nothing to do
            return self

        # record the entry
        self.record()

        # if i'm fatal
        if self.fatal:
            # complain
            raise self.complaint()

        # all done
        return self

    def complaint(self):
        """
        Prepare the exception i raise when i'm fatal
        """
        # instantiate the exception, with a copy of my entry
        complaint = self.fatalError(
            headline=f"{self.name}: {self.headline}",
            channel=self.name,
            page=self.page,
            notes=self.notes,
        )
        # and return it
        return complaint

    def outcome(self):
        """
        What recording an entry leads to: me, so the caller can keep going
        """
        # enable chaining
        return self

    def record(self):
        """
        Write the accumulated message to the device
        """
        # subclasses must override
        raise NotImplementedError(f"class '{type(self).__name__}' must implement 'record'")

    def newEntry(self, notes: dict | None = None):
        """
        Create a fresh message entry, starting from {notes} when they are given
        """
        # if there are notes to carry over
        if notes is not None:
            # get the entry factory
            from .Entry import Entry

            # make an entry with them; it keeps a copy of its own
            return Entry(notes=notes)

        # otherwise, initialize my metadata
        notes = {
            "channel": self.name,
            "severity": self.severity,
        }

        # inject whatever metadata it has
        notes.update(self.chronicler.notes)

        # get the entry factory
        from .Entry import Entry

        # make one
        entry = Entry(notes=notes)

        # and return it
        return entry

    # class data
    severity = "generic"  # the severity name
    headline = "generic"  # the summary of the condition when i'm fatal
    chronicler = Chronicler()  # the keeper of the global settings
    fatalError = JournalError  # the exception i raise when i'm fatal
    inventory_type = Inventory  # the type of the state shared by channels of the same name
    index = Index(active=False, fatal=False)  # the generic channel records nothing

    # instance data
    entry = None  # the accumulator of message content and metadata
    inventory = None  # the state shared by all instances of the same name/severity


# end of file
