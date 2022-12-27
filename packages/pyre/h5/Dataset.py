# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import journal
import pyre

# superclass
from .Object import Object


# the dataset descriptor base class
@pyre.schemata.typed
class Dataset(Object):
    """
    The base class of all dataset descriptors
    """

    # my mixins
    from .typed import bool, int, float, str, timestamp

    # public data
    @property
    def value(self):
        """
        Retrieve my value
        """
        # get the value from my cache
        value = self._value
        # if it's not set
        if value is None:
            # fall back to my default
            value = self.default
        # process it and return it
        return self.process(value=value)

    @value.setter
    def value(self, value):
        """
        Set my value
        """
        # process and cache the result
        self._value = self.process(value=value)
        # and done
        return

    @property
    def pyre_marker(self):
        """
        Generate an identifying mark
        """
        # use my type name
        return self.typename

    # interface
    def pyre_read(self):
        """
        Read my on-disk value into my cache
        """
        # if i'm not mapped to an h5 file
        if self.pyre_id is None:
            # make a channel
            channel = journal.warning("pyre.h5.sync")
            # complain
            channel.line(f"'{self.pyre_name}' is not synced to an h5 file")
            channel.line(f"while attempting to read '{self.pyre_location}'")
            # flush
            channel.log()
            # and return something harmless
            return None
        # if all is well, delegate
        return self.pyre_pull()

    def pyre_write(self):
        """
        Write my cache value to disk
        """
        # if i'm not mapped to an h5 file
        if self.pyre_id is None:
            # make a channel
            channel = journal.warning("pyre.h5.sync")
            # complain
            channel.line(f"'{self.pyre_name}' is not synced to an h5 file")
            channel.line(f"while attempting to write '{self.pyre_location}'")
            # flush
            channel.log()
            # and bail
            return
        # if all is well, delegate
        return self.pyre_push()

    # metamethods
    def __init__(self, value=None, **kwds):
        # chain up
        super().__init__(**kwds)
        # set up my {value}
        self._value = value
        # all done
        return

    def __str__(self):
        """
        Human readable representation
        """
        # easy enough
        return f"{self.pyre_location}: a dataset of type '{self.typename}'"

    # framework hooks
    def pyre_identify(self, authority, **kwds):
        """
        Let {authority} know i am a dataset
        """
        # attempt to
        try:
            # ask {authority} for my handler
            handler = authority.pyre_onDataset
        # if it doesn't exist
        except AttributeError:
            # chain up
            return super().pyre_identify(authority=authority, **kwds)
        # otherwise, invoke the handler
        return handler(dataset=self, **kwds)

    def pyre_clone(self, **kwds) -> "Dataset":
        """
        Make as faithful a clone of mine as possible
        """
        # invoke my constructor
        return super().pyre_clone(value=self.value, default=self.default, **kwds)

    # implementation details
    def pyre_pull(self):
        """
        Pull my on-disk value into my cache
        """
        # for now
        return None
        # my children know how to do this
        raise NotImplementedError(
            f"class '{type(self).__name__}' must implement 'pyre_pull'"
        )

    def pyre_push(self):
        """
        Push my cache value to disk
        """
        # for now
        return None
        # my children know how to do this
        raise NotImplementedError(
            f"class '{type(self).__name__}' must implement 'pyre_push'"
        )


# end of file
