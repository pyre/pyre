# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# externals
import enum


# declaration
class MemberStatus(enum.Enum):
    """
    Indicators used by team members to describe what happened during their execution
    """

    # as far as the team member can tell, all is good and it is ready to accept work
    healthy = 0
    # the team member is compromised and can't be relied upon any more; the task should be
    # rescheduled to another process; this worker should be removed from the pool permanently
    damaged = 1


# end of file
