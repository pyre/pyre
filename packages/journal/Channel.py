# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# externals
import traceback       # location information
# framework
import pyre            # for my superclass and {tracking}

# the index
from .Index import Index
# the base inventory
from .Inventory import Inventory
# the keeper of the global settings
from .Chronicler import Chronicler


# access to the channel shared state
class Channel(pyre.patterns.named):
    """
    Encapsulation of the per-channel shared state

    All channels of a given severity that have the same name access a common state object. This
    enables a type of context-free control of a channel: anybody with access to the name of a
    channel can control whether it's active, or what device it writes to.
    """


    # types
    from .exceptions import JournalError


    # public data
    detail = 1           # default detail


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
        # ask my inventory
        device = self.inventory.device
        # if it's non-trivial
        if device is not None:
            # that's the one
            return device
        # otherwise, return whatever the chronicler keeps
        return self.chronicler.device

    @device.setter
    def device(self, device):
        """
        Set my device
        """
        # hand it to my inventory
        self.inventory.device = device
        # all done
        return


    # control over the severity wide device
    @classmethod
    def getDefaultDevice(cls):
        """
        Get the default device associated with all channels of this severity
        """
        # my inventory type has it
        return cls.inventory_type.device


    @classmethod
    def setDefaultDevice(cls, device):
        """
        Get the default device associated with all channels of this severity
        """
        # get the previous setting
        old = cls.inventory_type.device
        # install the new device
        cls.inventory_type.device = device
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


    def line(self, message=""):
        """
        Add {message} to the current page
        """
        # add message to my page
        self.page.append(str(message))
        # all done
        return self


    def report(self, report):
        """
        Add lines from the {report} to the current page
        """
        # use {report} to extend my {page}
        self.page.extend(str(entry) for entry in report)
        # all done
        return self


    def log(self, message=None):
        """
        Add {message} to the current page and then record the entry
        """
        # if there is a final {message} to process
        if message is not None:
            # add it to the page
            self.page.append(str(message))

        # get a stack trace
        trace = traceback.extract_stack(limit=2)
        # so we can extract location information
        filename, line, function, *_ = trace[0]

        # decorate my current metadata
        notes = self.notes
        # with location information
        notes["filename"] = filename
        notes["line"] = str(line)
        notes["function"] = function

        # certain channels, e.g. errors and firewalls, raise exceptions as part of committing a
        # message to the journal. such exceptions may be caught and handled, and the channel
        # instance may continue to be used. this leads to text accumulating on my page, and the
        # next time i'm flushed, my {entry} still contains lines from the previous
        # message. the awkward block that follows attempts to prevent this by catching
        # exceptions, cleaning up the {entry} in the finally section, and re-raising the
        # exception. of course, if no exception is raised, we just clean up the page and move
        # on

        # carefully
        try:
            # commit the message to the journal and let the channel decide what to return to
            # the caller; currently, all channels return {self}, except {firewall}, which
            # returns the exception it would have raised if it were fatal
            status = self.commit()
        # if i'm a fatal diagnostic, {commit} raises a journal exception
        except self.JournalError:
            # no worries; someone else may know what to do
            raise
        # but in any case
        finally:
            # flush my entry
            self.entry = self.newEntry()

        # all done
        return status


    # metamethods
    def __init__(self, name, detail=detail, **kwds):
        # chain up
        super().__init__(name=name, **kwds)

        # set my detail
        self.detail = detail
        # look up my inventory
        self.inventory = self.index.lookup(name)
        # start out with an empty entry
        self.entry = self.newEntry()
        # and an invalid locator
        self.locator = None

        # all done
        return


    @classmethod
    def __init_subclass__(cls, active=True, fatal=False, **kwds):
        # chain up
        super().__init_subclass__(**kwds)

        # we will derive a customized class with a synthesized name
        name = cls.__name__ + Inventory.__name__
        # that is a subclass of {Inventory}
        bases = [ Inventory ]
        # with default values for the channel state
        attributes = {
            "active": active,
            "fatal": fatal,
            "device": None
            }
        # build the class
        inventory = type(name, tuple(bases), attributes)
        # fix the module so it gets the correct attribution in stack traces
        inventory.__module__ = cls.__module__
        # attach it as the inventory type
        cls.inventory_type = inventory

        # create one using my inventory type
        index = Index(inventoryType=inventory)
        # and attach it
        cls.index = index

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

        # record the entry and let the channel decide what to return to the user
        status = self.record()

        # if i'm fatal
        if self.fatal:
            # complain
            raise self.complaint()

        # all done
        return status


    def complaint(self):
        """
        Prepare the exception i raise when i'm fatal
        """
        # get my metadata
        notes = self.notes
        # pull the location information
        filename = notes["filename"]
        line = notes["line"]
        function = notes["function"]
        # build a locator
        self.locator = pyre.tracking.script(source=filename, line=line, function=function)
        # instantiate the exception
        complaint = self.fatalError(channel=self)
        # and return it
        return complaint


    def record(self):
        """
        Write the accumulated message to the device
        """
        # subclasses must override
        raise NotImplementedError(f"class '{type(self).__name__}' must implement 'record'")


    def newEntry(self):
        """
        Create a fresh message entry
        """
        # initialize my metadata
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
    severity = "generic"           # the severity name
    chronicler = Chronicler()      # the keeper of the global settings
    fatalError = JournalError      # the exception i raise when i'm fatal
    inventory_type = Inventory     # the default inventory type; subclasses get their own
    index = Index(inventory_type)  # the severity wide channel index

    # instance data
    entry = None                   # the accumulator of message content and metadata
    locator = None                 # location information
    inventory = None               # the state shared by all instances of the same name/severity


# end of file
