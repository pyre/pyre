# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# externals
import pyre
# my superclass
from .Executive import Executive


# declaration
class Web(Executive, family='pyre.shells.web'):
    """
    A shell enables application interactivity over the web
    """

    # user configurable state
    auto = pyre.properties.bool(default=True)
    auto.doc = 'controls whether to automatically launch the browser'


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
        # show me
        application.info.log('web server on {}'.format(address))
        # if we were asked to launch a browser
        if self.auto:
            # grab the package with the browser selection logic
            import webbrowser
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
