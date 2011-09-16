# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# meta class
from .Immutable import Immutable


# declaration
class Record(tuple, metaclass=Immutable):
    """
    The base class for representing data extracted from persistent stores.

    Records have field descriptors that provide the information necessary to convert data
    between the representation used by the persistent store and the native python object
    required by the application.

    Records are similar to named tuples: the underlying storage mechanism is a tuple, and the
    fields are descriptors that provide named access to the tuple entries. They are superior to
    named tuples since they enable the data model designer to specify types and constraints
    that must be satisfied by the data, and automate the conversion process to a large degree.

    Inheritance among {Record} subclasses is interpreted as composition: the set of fields that
    define a record is built out of the descriptors declared both locally and by all of its
    ancestors. Descriptor composition is subject to name shadowing.

    Records support {derivations}: fields whose value is computed using other record
    fields. Such fields are built automatically whenever a field declaration contains any sort
    of arithmetic on the right hand side.

    Details of the current implementation:

    * Storage for the record values is provided by {tuple}. This implies that indexed access
      using integers works as expected and does not require any special handling

    * Named access is handled through the field descriptors. Supporting composition via
      inheritance complicates the implementation a bit, as the rank of a given field is not
      known until the class mro is traversed and shadowing is taken into account. Each {Record}
      subclass maintains its own map from descriptor instances to the integer rank in the
      corresponding underlying tuple.
    """

 
    # types
    from .ConstAccessor import ConstAccessor as pyre_accessor
    # exceptions
    from ..constraints.exceptions import ConstraintViolationError


    # public data
    pyre_entries = () # a tuple with all my record entries, regardless of type
    pyre_fields = () # a tuple with all my fields
    pyre_derivations = () # a tuple with all my derivations

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
        return super().__new__(cls, data)

    
    # tuple construction
    @classmethod
    def pyre_processFields(cls, raw, **kwds):
        """
        Form the tuple that holds my values by extracting information either from {raw} or
        {kwds}, and walking the data through conversion, casting and validation.

        In the absence of derivations, the data tuple can be constructed by simply asking each
        field to consume one item from the raw input, convert it and place it in the record
        tuple
        """
        # if I were given an explicit tuple, build an iterator over it
        source = iter(raw) if raw is not None else (
            # otherwise, build a generator that extracts values from {kwds}
            kwds.pop(item.name, item.default) for item in cls.pyre_entries)
        # build the data tuple and return it
        return (item.extract(stream=source) for item in cls.pyre_entries)

            
    @classmethod
    def pyre_processFieldsAndDerivations(cls, raw, **kwds):
        """
        In the presence of derivations, things are a little more complicated: we must grant
        derivations access to the fields they depend on. To avoid casting, converting and
        validating the fields more than once, we maintain a cache with their values. An
        important step is performed by the metaclass: scanning derivation expressions and
        converting references to fields into field proxies
        """
        # if I were given an explicit tuple, build an iterator over it
        source = iter(raw) if raw is not None else (
            # otherwise, build a generator that extracts values from {kwds}
            kwds.pop(item.name, item.default) for item in cls.pyre_entries)
        # prepare my cache
        cache = {}
        # iterate over my items
        for item in cls.pyre_entries:
            # get the item to compute its value
            value = item.evaluate(stream=source, cache=cache)
            # and yield the value
            yield value
        # all done
        return


    # meta methods
    def __new__(cls, raw=None, **kwds):
        """
        Initialize a record using either the pre-qualified tuple {raw}, or by extracting the
        data from {kwds}
        """
        return super().__new__(cls, cls.pyre_processEntries(raw, **kwds))


# end of file 
