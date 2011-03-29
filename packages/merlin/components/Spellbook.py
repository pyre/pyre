# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# packages
import re
# access to the framework
import pyre


# declaration
class Spellbook(pyre.component, family="merlin.spellbook"):
    """
    This is a sample documentation string for Spellbook
    """

    # public state
    path = pyre.properties.array()
    path.doc = "the ordered list of directories with spells"


    # per instance public data


    # utilities
    def findSpells(self, pattern=None):
        # check whether the pattern starts with the name of one of the spell directories look
        # only there
        match = self._spelldirs.match(pattern) if pattern else None
        # if it does
        if match:
            # focus the search on the folder only
            folders = [ match.group(1) ]
            pattern = pattern[match.end():]
        # otherwise
        else:
            folders = self.spellpath
        # iterate through the spell locations
        for folder in folders:
            # look for spells
            for node, path in self.spells[folder].find(pattern=pattern):
                print(node.info.uri)
        # all done
        return


    # meta methods
    def __init__(self, **kwds):
        # chain to my ancestors
        super().__init__(**kwds)

        print(" ** spellbook initialization")
        print("    path: {.path!r}".format(self))
        # chain to my ancestors
        return


    # implementation details
    def _collectSpells(self, fileserver):
        """
        Traverse the application namespace looking for spells and cataloging them
        """
        # establish the folder
        spells = self.fileserver.newFolder()
        # mount it at the right spot
        self.fileserver['/merlin/spells'] = spells

        # look for the system spell directory
        try:
            # if all is well, this should succeed
            system = self.fileserver['/pyre/system/merlin/spells']
        except self.fileserver.NotFoundError as error:
            # something is wrong with the installation...
            system = self.fileserver.newFolder()
        # attach the system folder
        spells['system'] = system

        # now look for the user's spells
        try:
            # if the user has any spells
            user = self.fileserver['/pyre/user/merlin/spells']
        except self.fileserver.NotFoundError as error:
            # otherwise just build an empty folder
            user = self.fileserver.newFolder()
        # attach the user folder
        spells['user'] = user

        # finally, the project spells
        try:
            # does the project specify any spells?
            project = self.fileserver['/project/spells']
        except self.fileserver.NotFoundError as error:
            # something is wrong with the installation...
            project = self.fileserver.newFolder()
        # attach the project folder
        spells['project'] = project

        # and return it
        return spells


    # private data
    _spellpath = ('project', 'user', 'system')
    _spelldirs = re.compile('(' + "|".join(_spellpath) + ')/')


# end of file 
