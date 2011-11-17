# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


def fork(onParent, onChild):
    """
    Fork this process and invoke {onParent} in the main fork and {onChild} in the child fork
    """
    # access to fork
    import os
    # fork the process
    pid = os.fork()
    # in the parent process
    if pid > 0:
        # invoke the callable
        return onParent(pid=pid)
    # in the child process, find out my process id
    pid = os.getpid()
    # and invoke the callable
    return onChild(pid=pid)
    
    
def fork_pty(onParent, onChild):
    """
    Fork this process and invoke {onParent} in the main fork and {onChild} in the child fork
    """
    # access to fork
    import pty
    # fork the process
    pid, fd = pty.fork()
    # in the parent process
    if pid > 0:
        # invoke the callable
        return onParent(pid=pid, fd=fd)
    # in the child process, find out my process id
    pid = pty.os.getpid()
    # and invoke the callable
    return onChild(pid=pid)
    

# end of file 
