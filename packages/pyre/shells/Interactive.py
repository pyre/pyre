# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2017 all rights reserved
#


# access to the framework
import pyre
# my base class
from .Script import Script


class Interactive(Script, family="pyre.shells.interactive"):
    """
    A shell that invokes the main application behavior and then enters interactive mode
    """


    # interface
    @pyre.export
    def launch(self, application, *args, **kwds):
        """
        Invoke the application behavior
        """
        # show the application help screen
        application.help()
        # enter interactive mode
        status = self.pyre_interactiveSession(application=application)
        # all done
        return status


    # implementation details
    def pyre_interactiveSession(self, application, context=None):
        """
        Convert this session to an interactive one
        """
        # we need an application specific tag
        name = application.pyre_namespace or application.pyre_name or 'pyre'

        # try to
        try:
            # get readline
            import readline
        # if not there
        except ImportError:
            # no problem
            pass
        # if successful
        else:
            # turn on completion
            import rlcompleter
            # check which interface is available and do the right thing: on OSX, readline is
            # provided by libedit
            if 'libedit' in readline.__doc__:
                # enable completion
                readline.parse_and_bind('bind -v')
                readline.parse_and_bind('bind ^I rl_complete')
            # on other machines, or if the python readline extension is available on OSX
            else:
                # enable completion
                readline.parse_and_bind('tab: complete')

            # build the uri to the history file
            history = pyre.primitives.path('~', '.{}-history'.format(name)).expanduser().resolve()
            # stringify
            history = str(history)
            # attempt to
            try:
                # read it
                readline.read_history_file(history)
            # if not there
            except IOError:
                # no problem
                pass
            # make sure it gets saved
            import atexit
            # by registering a handler for when the session terminates
            atexit.register(readline.write_history_file, history)

        # go live
        import code, sys
        # adjust the prompts
        sys.ps1 = '{}: '.format(name)
        sys.ps2 = '  ... '

        # prime the local namespace
        context = context or {}
        # adjust it
        context['app'] = application
        # give the application an opportunity to add symbols as well
        context = application.pyre_interactiveSessionContext(context=context)
        # enter interactive mode
        return code.interact(banner=application.pyre_interactiveBanner(), local=context)


# end of file
