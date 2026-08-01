# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the outcome of a verification pass
class Audit:
    """
    The structured outcome of re-proving the installations in a resolution report

    Discovery proves a recipe's markers against what the package database reported;
    verification proves them against what the installation says now, so it catches
    configuration that points at artifacts that are not there, installations that were
    removed after they were discovered, and user overrides that a discovery time check
    cannot see. {verified} lists the categories whose markers all resolved, in report
    order; {broken} maps the rest to their complaints
    """

    # interface
    @property
    def clean(self):
        """
        Check whether everything the report asked for is usable
        """
        # nothing may be broken
        if self.broken:
            # or the audit is not clean
            return False
        # and the resolution itself must have panned out
        report = self.report
        # with nothing left unaccounted for
        return not (report.unsupported or report.unavailable or report.conflicted)

    # meta-methods
    def __init__(self, *, report, **kwds):
        """
        Prime an empty audit of the given {report}
        """
        # chain up
        super().__init__(**kwds)
        # the resolution outcome under audit
        self.report = report
        # the categories whose markers all resolved
        self.verified = []
        # the map from broken categories to their complaints
        self.broken = {}
        # all done
        return

    # debugging support
    def __str__(self):
        # summarize the outcome
        return f"verified {len(self.verified)} categories; {len(self.broken)} broken"

    # narrow the footprint
    __slots__ = ("report", "verified", "broken")


# end of file
