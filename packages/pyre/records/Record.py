# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# my metaclass
from .Templater import Templater

# superclass
from ..framework.Dashboard import Dashboard


# declaration
class Record(Dashboard, metaclass=Templater):
    """
    The base class for representing data extracted from persistent stores.

    Records have field descriptors that provide the information necessary to convert data
    between the representation used by the persistent store and the native python object
    required by the application.

    Records are similar to named tuples: the underlying storage mechanism is a tuple, and the
    fields are descriptors that provide named access to the tuple items. They are superior to
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
    # exceptions
    from ..constraints.exceptions import ConstraintViolationError
    from .exceptions import AmbiguousColumnError, MissingColumnError

    # public data; patched by the metaclass
    pyre_name = None  # the name of the record
    # structure
    pyre_localFields = None  # the tuple of locally declared record fields
    # the full piles that include inherited entries
    pyre_fields = None  # the tuple of all accessible fields, both local and inherited
    pyre_measures = None  # the tuple of all primary fields
    pyre_derivations = None  # the tuple of fields whose values are computed on the fly
    # a map from field descriptors to their column index
    pyre_columns = None
    # a map from each inherited field a redeclaration shadows to the field that replaces it
    pyre_shadows = None

    # interface; patched by the metaclass
    @classmethod
    def pyre_immutable(cls, data=None, **kwds):
        """
        Build an immutable instance
        """
        # easy enough
        return cls.pyre_immutableTuple(record=cls, data=data, **kwds)

    @classmethod
    def pyre_mutable(cls, data=None, **kwds):
        """
        Build a mutable instance
        """
        # easy enough
        return cls.pyre_mutableTuple(record=cls, data=data, **kwds)

    # support for readers that want to match their headers to my fields
    @classmethod
    def pyre_selectColumns(cls, headers):
        """
        Find the column of each of my measures among {headers}, the names of the columns of a
        source in order, and yield its offset, or {None} for an optional measure the source
        lacks

        Each measure matches the columns named after any of its aliases, so a source can name
        its columns differently than my fields are named; a measure that matches more than one
        column is an error, and so is a required measure that matches none
        """
        # go through my measures
        for measure in cls.pyre_measures:
            # find the columns named after any of its aliases
            columns = [
                (offset, header)
                for offset, header in enumerate(headers)
                if header in measure.aliases
            ]
            # a measure that matches more than one
            if len(columns) > 1:
                # cannot tell which one holds its values
                raise cls.AmbiguousColumnError(record=cls, field=measure, columns=columns)
            # a measure that matches exactly one
            if columns:
                # reads from it
                ((offset, _),) = columns
                # so hand its offset over
                yield offset
                # and move on
                continue
            # an optional measure that matches none
            if measure.optional:
                # takes its default, which the reader supplies
                yield None
                # and move on
                continue
            # a required measure that matches none has nowhere to read its values from
            raise cls.MissingColumnError(record=cls, field=measure, headers=headers)
        # all done
        return


# end of file
