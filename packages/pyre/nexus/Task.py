# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


class Task:
    """
    Encapsulation of a task that is to be distributed to a worker for asynchronous execution
    """


    # types
    from .exceptions import RecoverableError
    from .TaskStatus import TaskStatus as taskcodes
    from .CrewStatus import CrewStatus as crewcodes


    # meta-methods
    def __call__(self, **kwds):
        # delegate
        return self.execute(**kwds)


    # implementation details
    def execute(self, **kwds):
        # nothing else to do
        return


# end of file
