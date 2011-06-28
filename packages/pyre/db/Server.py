# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# packages
import pyre
import pyre.weaver
from . import datastore, sql


# declaration
class Server(pyre.component, implements=datastore):
    """
    Abstract component that encapsulates the connection to a database back end

    This class is meant to be used as the base class for back end specific component
    implementations. It provides a complete but trivial implementation of the {DataStore}
    interface.
    """


    # traits
    sql = pyre.properties.facility(interface=pyre.weaver.language, default=sql)
    sql.doc = "the generator of the SQL statements"


    # required interface
    @pyre.export
    def attach(self):
        """
        Connect to the database back end
        """
        raise NotImplementedError(
            "class {.__class__.__name__!r} must override 'attach'".format(self))


    # meta methods
    # context manager support
    def __enter__(self):
        """
        Hook invoked when the context manager is entered
        """
        return self


    def __exit__(self, exc_type, exc_instance, exc_traceback):
        """
        Hook invoked when the context manager's block exits
        """
        # re-raise any exception that occurred while executing the body of the with statement
        return False


# end of file 
