# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


"""
This package provides support for composing pyre applications

The pyre framework encourages factoring applications into two distinct parts: a subclass of the
component {Application} that defines the runtime behavior of the application, and a hosting
strategy that defines the runtime environment in which the application executes. The hosting
strategy is a subclass of the component {Shell} and is responsible for creating the execution
context for the application.

The package provides a number of ready to use hosting strategies.

{Script} expects an instance of an {Application} subclass, invokes its {main} method, and exits
after handing the value returned to the operating system as the process exit code. It the pyre
equivalent of the familiar launching of executables written in low level languages.

{Daemon} is suitable for applications that run in the background, without access to a
terminal. It performs the steps necessary to detach a process from its parent so that the
parent may exit without causing the child to terminate as well.

{Service} builds on {Daemon} to enable distributed applications by exposing the application
component registry to the network.

Other packages leverage these building blocks to provide support for other hosting
strategies. For a sophisticated example, see the {mpi} package, which provides support for
running concurrent applications using {MPI}.
"""


# the protocols
from .Shell import Shell as shell
from .Action import Action as action

# command implementations
from .Command import Command as command
from .Panel import Panel as panel

# the hosting strategies
from .Script import Script as script
from .Fork import Fork as fork
from .Daemon import Daemon as daemon

# terminal support
from .Terminal import Terminal as terminal
from .ANSI import ANSI as ansi
from .Plain import Plain as plain

# the base application components
from .Application import Application as application
from .Plexus import Plexus as plexus
# and its support
from .Layout import Layout as layout

# the user component
from .User import User as user


# end of file 
