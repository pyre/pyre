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

    # value access
    @property
    def value(self):
        """
        Retrieve my value
        """
        # read my cache
        value = self._value
        # if it's non trivial
        if value is not None:
            # hand it off
            return value
        # otherwise, read from disk
        return self._pyre_pull()

    @value.setter
    def value(self, value):
        """
        Store my value
        """
        # process the incoming value and store it
        self._value = self._pyre_layout.process(value)
        # all done
        return

    # metadata
    @property
    def cell(self):
        """
        The dataset cell type, a DataSetType enum
        """
        # easy enough
        return self._pyre_id.cell

    @property
    def disksize(self):
        """
        The on-disk size of the dataset
        """
        # easy enough
        return self._pyre_id.disksize

    @property
    def memsize(self):
        """
        The in-memory size of the dataset
        """
        # easy enough
        return self._pyre_id.memsize

    @property
    def offset(self):
        """
        The offset of this dataset on disk
        """
        # easy enough
        return self._pyre_id.offset

    @property
    def shape(self):
        """
        The dataset shape
        """
        # easy enough
        return self._pyre_id.shape

    @property
    def space(self):
        """
        The dataset space
        """
        # easy enough
        return self._pyre_id.space

    @property
    def type(self):
        """
        The dataset type
        """
        # easy enough
        return self._pyre_id.type

    # metamethods
    def __init__(self, layout=None, **kwds):
        # chain up
        super().__init__(layout=layout, **kwds)
        # initialize my value cache
        self._value = None
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
            return
        # if i don't have a type descriptor
        if self._pyre_layout is None:
            # make a channel
            channel = journal.warning("pyre.h5.sync")
            # complain
            channel.line(f"{self}")
            channel.line(f"does not have a type")
            channel.line(f"while reading '{file._pyre_uri}'")
            # flush
            channel.log()
            # and return something harmless
            return
        # if all is well, attempt to
        try:
            # read the value and update my cache
            return self._pyre_pull()
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
        # all done
        return

    def _pyre_write(self, file: "File", src: "Dataset"):
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
        self._pyre_push(src=src)
        # all done
        return

    # lower level value syncing with no error checking
    def _pyre_pull(self):
        """
        Extract my value from disk
        """
        # get my spec
        spec = self._pyre_layout
        # if i don't have one
        if spec is None:
            # there isn't much more i can do
            return None
        # get my h5 handle
        hid = self._pyre_id
        # if i don't have a connection to a file
        if hid is None:
            # process and return my default value; don't cache it so we can try again next
            # time the value is requested
            return spec.process(spec.default)
        # if all is good, ask my spec to extract my value from the h5 store and process it
        value = spec._pyre_pull(dataset=self)
        # update the cache
        self._value = value
        # and hand it off
        return value

    def _pyre_push(self, src):
        """
        Flush my value  to disk
        """
        # get my layout
        layout = self._pyre_layout
        # ask it to flush me to disk
        layout._pyre_push(src=src, dest=self)
        # all done
        return

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
