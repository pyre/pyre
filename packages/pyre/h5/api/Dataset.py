# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import journal

# superclass
from .Object import Object


# a basic h5 object
class Dataset(Object):
    """
    Access to the data stored in an h5 file
    """

    # datasets are scalars, by default
    shape = "scalar"

    # value access
    @property
    def value(self):
        """
        Retrieve my value
        """
        # easy enough
        return self._value

    @value.setter
    def value(self, value):
        """
        Store my value
        """
        # process the incoming value and store it
        self._value = self._pyre_layout.process(value)
        # all done
        return

    # metamethods
    def __init__(self, layout=None, **kwds):
        # chain up
        super().__init__(layout=layout, **kwds)
        # initialize my value
        self._value = layout.process(layout.default)
        # all done
        return

    def __str__(self):
        """
        Human readable representation
        """
        # easy enough
        return f"dataset at '{self._pyre_location}' of type '{self._pyre_layout.type}'"

    # framework hooks
    # value syncing
    def _pyre_read(self, file):
        """
        Read my on-disk value into my cache
        """
        # if i'm not bound to an h5 source
        if self._pyre_id is None:
            # make a channel
            channel = journal.warning("pyre.h5.sync")
            # complain
            channel.line(f"{self}")
            channel.line(f"is not bound to an h5 file")
            channel.line(f"while reading '{file._pyre_uri}'")
            # flush
            channel.log()
            # and return something harmless
            return None
        # if all is well, attempt to
        try:
            # read the value and update the cache
            self.value = self._pyre_pull()
        # if this fails
        except NotImplementedError as error:
            # make a channel
            channel = journal.warning("pyre.h5.sync")
            # complain
            channel.line(f"{self}")
            channel.line(f"{error}")
            channel.line(f"can't pull values from disk")
            channel.line(f"while reading '{file._pyre_uri}'")
            # flush
            channel.log()
        # and return something harmless, in case errors aren't fatal
        return None

    def _pyre_pull(self):
        """
        Extract my value from disk and populate my cache
        """
        # get my layout
        layout = self._pyre_layout
        # ask it to extract the value from the h5 store and process it
        value = layout._pyre_pull(dataset=self)
        # hand it off
        return value

    def _pyre_write(self, file):
        """
        Write my cache value to disk
        """
        # if i'm not mapped to an h5 file
        if self._pyre_id is None:
            # make a channel
            channel = journal.warning("pyre.h5.sync")
            # complain
            channel.line(f"{self}")
            channel.line(f"is not bound to an h5 file")
            channel.line(f"while writing '{file._pyre_uri}'")
            # flush
            channel.log()
            # and bail
            return
        # if all is well, delegate
        return self._pyre_layout._pyre_push(datset=self)

    # visiting
    def _pyre_identify(self, authority, **kwds):
        """
        Let {authority} know i am a dataset
        """
        # attempt to
        try:
            # ask {authority} for my handler
            handler = authority._pyre_onDataset
        # if it doesn't understand
        except AttributeError:
            # chain up
            return super()._pyre_identify(authority=authority, **kwds)
        # otherwise, invoke the handler
        return handler(dataset=self, **kwds)


# end of file
