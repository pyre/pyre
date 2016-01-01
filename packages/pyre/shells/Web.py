# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# externals
import pyre
import webbrowser
# my superclass
from .Executive import Executive


# declaration
class Web(Executive, family='pyre.shells.web'):
    """
    A shell enables application interactivity over the web
    """


    # interface
    @pyre.export
    def launch(self, application, *args, **kwds):
        """
        Invoke the {application} behavior
        """
        # create a nexus
        nexus = pyre.nexus.node()
        # attach it to the application
        application.nexus = nexus
        # register it with the nexus
        nexus.services['web'] = 'http'
        # activate
        nexus.activate(application=application)

        # get the address of the web server
        address = nexus.services['web'].address
        # form a url
        url = 'http://localhost:{.port}/'.format(address)
        # launch the browser
        webbrowser.open(url)

        # set up a net
        try:
            # get the nexus to do its thing
            # N.B. this is an infinite loop; it is the responsibility of the application to
            # terminate the interaction with the user and exit gracefully
            status = nexus.serve()
        # if the user interrupted
        except KeyboardInterrupt as event:
            # launch the handler
            status = application.pyre_interrupted(info=event)

        # in any case, we are all done
        return status


# end of file
