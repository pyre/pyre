# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# externals
import itertools
# access to the framework
import pyre


# class declaration
class Action(pyre.protocol, family='pyre.actions'):
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


    # support for framework requests
    @classmethod
    def pyre_searchpath(cls):
        """
        Return an iterable over the action locations
        """
        # use the pyre configuration path
        return (folder.address for folder in cls.pyre_configurator.configpath)


    @classmethod
    def pyre_actionFolders(cls):
        """
        Return an iterable over the action folder names
        """
        # get my context resolver
        resolver = cls.pyre_contextResolver()
        # ask it to build a path out of my family name fragments and return it
        yield resolver.join(*cls.pyre_familyFragments())
        # all done
        return


    @classmethod
    def pyre_documentedActions(cls):
        """
        Retrieve all visible implementations that are documented
        """
        # get all visible implementations
        for uri, name, action in cls.pyre_locateAllImplementers():
            # get the tip
            tip = action.pyre_tip
            # if there is one
            if tip:
                # pass this one along
                yield uri, name, action, tip
        # all done
        return


# end of file
