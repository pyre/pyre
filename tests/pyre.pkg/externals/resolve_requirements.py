#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
The resolver accepts text specifications and structured requirements interchangeably

The configuration file {resolve_requirements.yaml} restricts the host to the bare engine
over the fixture installation
"""

# support
import pyre


# the application
class resolve_requirements(pyre.application):
    """
    An application that resolves its requirements explicitly
    """


def test():
    """
    Resolve a mixed request and verify the report speaks the requirement vocabulary
    """
    # instantiate the application; this loads {resolve_requirements.yaml}
    app = resolve_requirements(name="resolve_requirements")
    # a structured requirement
    structured = pyre.externals.requirement.parse("metis")
    # resolve a request that mixes text and structure
    report = pyre.externals.resolve(requested=["parmetis", structured])
    # the request is echoed back in structured form
    assert all(isinstance(req, pyre.externals.requirement) for req in report.requested)
    # the closure was realized in full
    assert set(report.selections) == {"parmetis", "metis", "mpi"}
    # nothing was conflicted
    assert not report.conflicted
    # and the dependency edges arrived as structured requirements too
    parmetis = report.selections["parmetis"]
    assert all(isinstance(req, pyre.externals.requirement) for req in parmetis.dependencies)

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
