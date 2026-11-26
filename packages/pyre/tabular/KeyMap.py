# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


class KeyMap:
    """
    The map from the values in a column of primary keys of a sheet to the rows that hold them

    Rows whose key is unset are left out until they get one. The keys of mutable rows may change
    after the rows join the sheet; I watch them, and rebuild the map on the first lookup after a
    change
    """

    # exceptions
    from .exceptions import DuplicateKeyError

    # interface
    def check(self, record):
        """
        Make sure that the key of {record}, a row about to join my sheet, is not there already
        """
        # get the key
        key = record[self.index]
        # an unset key is never a duplicate
        if key is None:
            # so there is nothing to check
            return self
        # bring the map up to date
        self.refresh()
        # if another row holds this key
        if key in self.rows:
            # complain
            raise self.DuplicateKeyError(sheet=self.sheet, field=self.field, key=key)
        # all done
        return self

    def add(self, row, record):
        """
        Map the key of {record}, which just joined my sheet as {row}, and watch it for changes
        """
        # get the key; reading it also means that its next change will be announced
        key = record[self.index]
        # if it is set
        if key is not None:
            # map it to its row
            self.rows[key] = row
        # watch the key for changes
        record.pyre_observe(index=self.index, observer=self)
        # all done
        return self

    def locate(self, key):
        """
        Find the row of my sheet that holds {key}
        """
        # bring the map up to date
        self.refresh()
        # and look up the key
        return self.rows[key]

    def refresh(self):
        """
        Rebuild the map, if a key changed since it was last built
        """
        # if the map is current
        if not self.stale:
            # there is nothing to do
            return self
        # start a new map
        rows = {}
        # go through the rows of my sheet
        for row, record in enumerate(self.sheet.pyre_data):
            # get the key; reading it also means that its next change will be announced
            key = record[self.index]
            # rows whose key is unset
            if key is None:
                # stay out of the map
                continue
            # if another row holds this key
            if key in rows:
                # complain, leaving the map stale until the conflict is resolved
                raise self.DuplicateKeyError(sheet=self.sheet, field=self.field, key=key)
            # otherwise, map the key to its row
            rows[key] = row
        # install the new map
        self.rows = rows
        # and mark it current
        self.stale = False
        # all done
        return self

    # notifications
    def flush(self, **kwds):
        """
        Handle the notice that the key of one of the rows of my sheet changed
        """
        # mark the map as stale; it is rebuilt on the next lookup
        self.stale = True
        # all done
        return self

    # meta-methods
    def __init__(self, sheet, field, index, **kwds):
        """
        Map the values of {field}, which sit in column {index} of {sheet}, to their rows
        """
        # chain up
        super().__init__(**kwds)
        # save the sheet
        self.sheet = sheet
        # the field
        self.field = field
        # and its column
        self.index = index
        # start with an empty map
        self.rows = {}
        # that is current
        self.stale = False
        # all done
        return


# end of file
