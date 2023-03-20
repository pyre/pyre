# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


"""
Definitions for all the exceptions raised by this package
"""


# superclass
from ..exceptions import H5Error


# the local base of api errors
class APIError(H5Error):
    """
    The base class of all exceptions raised by the {h5.api} package
    """


# datatypes
class UnsupportedTypeError(APIError):
    """
    Exception raised when type deduction bumps into an unsupported type
    """

    # the message template
    description = "'{0.dataset}': unsupported type '{0.h5type.name}'"

    # metamethods
    def __init__(self, dataset, h5type, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the error information
        self.dataset = dataset
        self.h5type = h5type
        # all done
        return


class UnsupportedCompoundTypeError(APIError):
    """
    Exception raised when type deduction bumps into an unsupported compound type
    """

    # the message template
    description = "{0.dataset}: dataset of unsupported compound type"

    # metamethods
    def __init__(self, dataset, h5type, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the error information
        self.dataset = dataset
        self.h5type = h5type
        # all done
        return

    # framework hooks
    def _pyre_report(self, **kwds):
        """
        Generate a detailed report
        """
        # chain up to prime the report
        yield from super()._pyre_report()
        # introduce the details that follow
        yield "with fields:"
        # get the type
        h5type = self.h5type
        # go through the type members
        for m in range(h5type.members):
            # get the name
            name = h5type.name(m)
            # type
            type = h5type.type(m).cell.name
            # and offset
            offset = h5type.offset(m)
            # show me
            yield f"  '{name}': a {type} at offset {offset}"
        # all done
        return


# type mismatch
class TypeMismatchError(APIError):
    """
    Exception raised whet the on-disk type of a dataset is not compatible with its specification
    """

    # the message template
    description = (
        "at '{0.path}': type mismatch: "
        "expected '{0.expected.disktype.cell.name}', "
        "got '{0.actual.disktype.cell.name}'"
    )

    # metamethods
    def __init__(self, path, expected, actual, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the error information
        self.path = path
        self.expected = expected
        self.actual = actual
        # all done
        return


# validator errors
class ValidationError(APIError):
    """
    Intermediate class for validation error reports
    """

    # metamethods
    def __init__(self, spec, location, **kwds):
        # chain  up
        super().__init__(**kwds)
        # save the error information
        self.spec = spec
        self.location = location
        # all done
        return

    # framework hooks
    def _pyre_report(self, **kwds):
        """
        Generate a detailed report
        """
        # chain up to let my superclasses contribute
        yield from super()._pyre_report(**kwds)
        # when
        yield f"while comparing {self.location}"
        yield f"against {self.spec}"
        # all done
        return


# category mismatch
class CategoryMismatchError(ValidationError):
    """
    Exception raised when there is a category mismatch between the specification
    and the H5 product contents
    """

    # the message template
    description = (
        "at '{0.location._pyre_location}': expected {0.expected}, got {0.actual} "
    )

    # metamethods
    def __init__(self, actual, expected, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the error information
        self.actual = actual
        self.expected = expected
        # all done
        return


# missing or excess group members
class GroupMembershipError(ValidationError):
    """
    Exception raised when there is a discrepancy in membership between the
    specification of a group and its on-disk contents
    """

    # the message template
    description = "at '{0.location._pyre_location}': excess or missing group members"

    # metamethods
    def __init__(self, extra, missing, **kwds):
        # chain up
        super().__init__(**kwds)
        # record
        self.extra = extra
        self.missing = missing
        # all done
        return

    # framework hooks
    def _pyre_report(self):
        """
        Generate a detailed report
        """
        # chain up
        yield from super()._pyre_report()
        # get the extra names
        extra = self.extra
        # if there are any
        if extra:
            # make a pretty pile
            names = ", ".join(f"'{name}'" for name in self.extra)
            # and report
            yield f"extra: {names}"
        # get the missing names
        missing = self.missing
        # if there are any
        if missing:
            # make a pretty pile
            names = ", ".join(f"'{name}'" for name in self.missing)
            # add them to the report
            yield f"missing: {names}"
        # all done
        return


# end of file
