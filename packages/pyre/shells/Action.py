# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# access to the framework
import pyre


# class declaration
class Action(pyre.protocol, family="pyre.actions"):
    """
    A protocol that facilitates application extensibility: components that implement {Action}
    can be invoked from the command line
    """

    # types
    from pyre.schemata import uri

    # expected interface
    @pyre.provides
    def main(self, *kwds):
        """
        This is the implementation of the action
        """

    @pyre.provides
    def help(self, **kwds):
        """
        Provide help with invoking this action
        """

    @classmethod
    def pyre_actions(cls, plexus):
        """
        Retrieve all visible implementations
        """
        # get the search context from the {plexus}
        namespace = plexus.pyre_package().name
        # get all visible implementations
        for uri, name, action in cls.pyre_locateAllImplementers(namespace=namespace):
            # attempt to
            try:
                # get the tip
                tip = action.pyre_tip
            # if there isn't one
            except AttributeError:
                # set one up
                tip = None
            # pass it along
            yield uri, name, action, tip
        # all done
        return

    @classmethod
    def pyre_documentedActions(cls, plexus):
        """
        Retrieve all visible implementations that are documented
        """
        # get all implementations
        for uri, name, action, tip in cls.pyre_actions(plexus=plexus):
            # if this action is not documented
            if not tip:
                # assume it is not part of the public interface and skip it
                continue
            # otherwise, pass it along
            yield uri, name, action, tip
        # all done
        return


# end of file
