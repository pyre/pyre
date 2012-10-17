# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


class NamedTuple(tuple):
    """
    Base class for the two record types declared in this package.

    This class is used to establish the common layout of records. Its instances are not
    directly useful, so please do not instantiate.
    """


    # exceptions
    from ..constraints.exceptions import ConstraintViolationError
    

    # public data
    pyre_entries = () # a tuple with all my record entries, regardless of type
    pyre_fields = () # a tuple with all my fields
    pyre_derivations = () # a tuple with all my derivations
    pyre_localEntries = () # a tuple with all the record entries that show up in my declaration

    pyre_index = None # the map of descriptors to indices
    pyre_processEntries = None # the data processing algorithm


    # interface
    @classmethod
    def pyre_selectColumns(cls, headers):
        """
        Prepare a tuple of the column numbers needed to populate my instances, given a map
        (column name) -> (column index).

        This enables the managers of the various persistent stores to build record instances
        from a subset of the information they have access to. It is also designed to perform
        column name translations from whatever meta data is available in the store to the
        canonical record field names
        """
        # iterate over my fields
        for field in cls.pyre_fields:
            # and over its aliases
            for alias in field.aliases:
                # if this alias appears in the headers
                try:
                    # compute the column index and return it
                    yield headers[alias]
                    # get the next field
                    break
                except KeyError:
                    continue
            # error: unable to find a source for this field
            else:
                msg = "unable to find a source for field {!r}".format(field.name)
                import journal
                raise journal.firewall("pyre.records").log(msg)
        # all done
        return


    # fast but dangerous short-cut to record creation
    @classmethod
    def pyre_raw(cls, data):
        """
        Bypass casting, conversions and validations for those special clients that know their
        data is good. Use with caution
        """
        raise NotImplementedError(
            "class {.__name__!r} must implement 'pyre_raw'".format(cls))
    

# end of file 
