# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import collections.abc


# class declaration
class Headers(collections.abc.MutableMapping):
    """
    A case insensitive mapping of HTTP header field names to their values

    HTTP field names are case insensitive (RFC 7230), so every lookup ignores case; the casing
    each name was stored with is remembered so that iteration and serialization reproduce it
    """

    # meta-methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # the backing store maps the lower cased name to an (original name, value) pair; a plain
        # dict preserves insertion order, which the response serializer relies on
        self._fields = {}
        # all done
        return

    def __getitem__(self, name):
        """
        Retrieve the value stored under {name}, regardless of its case
        """
        # look up by the case insensitive key and hand back the value half of the pair
        return self._fields[name.lower()][1]

    def __setitem__(self, name, value):
        """
        Store {value} under {name}, remembering the casing the caller used
        """
        # key by the lower cased name, but keep the original around for later reproduction
        self._fields[name.lower()] = (name, value)
        # all done
        return

    def __delitem__(self, name):
        """
        Remove the field stored under {name}, regardless of its case
        """
        # drop the entry under its case insensitive key
        del self._fields[name.lower()]
        # all done
        return

    def __iter__(self):
        """
        Iterate over the field names in the casing they were stored with
        """
        # yield the original name from each stored pair
        return (name for name, _ in self._fields.values())

    def __len__(self):
        """
        Count the stored fields
        """
        # delegate to the backing store
        return len(self._fields)

    def __contains__(self, name):
        """
        Check whether a field named {name} is present, regardless of its case
        """
        # consult the backing store with the case insensitive key
        return name.lower() in self._fields

    def __repr__(self):
        """
        Build a faithful representation
        """
        # show the original names alongside their values
        return f"{type(self).__name__}({dict(self.items())!r})"


# end of file
