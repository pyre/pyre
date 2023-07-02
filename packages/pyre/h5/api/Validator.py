# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import journal

# superclass
from .Reader import Reader

# the validation error types
from . import exceptions

# typing
import typing
from .. import schema
from .Dataset import Dataset
from .Group import Group
from .Location import Location

# type aliases
ErrorReport = typing.List[Exception]


# content validator
class Validator(Reader):
    """
    A visitor that compares the contents of an h5 location with its specification
    """

    # interface
    def validate(
        self,
        location: Location,
        spec: schema.descriptor,
        report: typing.Optional[ErrorReport] = None,
    ) -> ErrorReport:
        """
        Generate a report of the deviation of {location} from its {spec}
        """
        # initialize the report, if necessary
        report = [] if report is None else report
        # ask the {spec} descriptor to identify itself
        spec._pyre_identify(authority=self, location=location, report=report)
        # make a channel
        channel = journal.warning("pyre.h5.api.validator")
        # go through the errors
        for complaint in report:
            # and print each one out
            channel.report(report=complaint._pyre_report())
            # separated by blank lines
            channel.line()
        # flush
        channel.log()
        # all done
        return report

    # framework hooks
    # implementation of the {descriptor} visitor
    def _pyre_onGroup(
        self, group: schema.group, location: Group, report: ErrorReport
    ) -> ErrorReport:
        """
        Validate {location} against its {group} spec
        """
        # if {location} is not a group
        if not isinstance(location, Group):
            # get its type
            locationCls = type(location)
            # build a description of the problem
            problem = exceptions.CategoryMismatchError(
                spec=group,
                location=location,
                expected="group",
                actual=f"'{locationCls.__module__}.{locationCls.__name__}'",
            )
            # add it to the report
            report.append(problem)
            # and go no further
            return report

        # get the {group} table with the h5 to attribute name translations
        aliases = group._pyre_aliases
        # ask the {group} for all known descriptor names
        expected = set(aliases.keys())
        # ask the {location} for the names and types of the group members as recorded on-disk
        actual = set(location._pyre_id.members())
        # separate them into piles
        common = expected & actual
        missing = expected - actual
        extra = actual - expected
        # if there is a discrepancy
        if missing or extra:
            # specify the problem
            problem = exceptions.GroupMembershipError(
                spec=group, location=location, extra=extra, missing=missing
            )
            # and add it to the report
            report.append(problem)

        # go through the common names only; nothing more can be done with the rest
        for name in common:
            # build content by looking only at the disk
            child = location._pyre_find(path=name)
            # look up the corresponding node in my spec
            spec = getattr(group, aliases[name])
            # and validate each one
            spec._pyre_identify(authority=self, location=child, report=report)

        # all done
        return report

    def _pyre_onDataset(
        self, dataset: schema.dataset, location: Dataset, report: ErrorReport
    ) -> ErrorReport:
        """
        Validate {location} against its {dataset} spec
        """
        raise NotImplementedError("NYI!")
        # all done
        return report


# end of file
