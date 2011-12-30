# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# externals
import os
import merlin


# declaration
class Initializer(merlin.spell):
    """
    Create a new merlin project rooted at the given directory
    """


    # public state
    project = merlin.properties.str(default=None)
    project.doc = 'the name of the project'

    createPrefix = merlin.properties.bool(default=False)
    createPrefix.aliases.add('create-prefix')
    createPrefix.doc = 'create all directories leading up to the specified target'

    force = merlin.properties.bool(default=False)
    force.doc = 'initialize the target folder regardless of whether is it already part of a project'

    # class interface
    # interface
    @merlin.export
    def main(self, *args, **kwds):
        """
        Make {folder} the root of a new merlin project. The target {folder} is given as an
        optional command line argument, and defaults to the current directory. Issue an error
        message if {folder} is already a merlin project.
        """
        # NYI: non-local uris
        # access my executive
        merlin = self.merlin

        # the first argument is supposed to be the target folder that will hold the new project
        folder = args[0] if args else os.curdir

        # first check whether this directory is already part of a merlin project
        root, metadir = merlin.locateProjectRoot(folder=folder)
        # if it is
        if root and not self.force:
            # complain
            import journal
            msg = '{!r} is already within an existing project'.format(folder)
            return journal.error('merlin.init').log(msg)

        # if the directory does not exist
        if not os.path.isdir(folder):
            import journal
            msg = 'target folder {!r} does not exist; creating'.format(folder)
            journal.info('merlin.init').log(msg)
            # were we asked to build all parent directories?
            if self.createPrefix:
                # yes, do it
                os.makedirs(os.path.abspath(folder))
            # otherwise
            else:
                # attempt
                try:
                    # to create the directory
                    os.mkdir(folder)
                # if that fails
                except OSError:
                    # complain
                    import journal
                    msg = 'could not create folder {!r}'.format(folder)
                    return journal.error('merlin.init').log(msg)

        # now that it's there, build a local filesystem around it
        pfs = self.vfs.local(root=folder)

        # build a virtual filesystem so we can record the directory layout
        mfs = self.vfs.virtual()
        # here is the directory structure
        mfs['spells'] = mfs.folder()

        # attempt to
        try:
            # realize the layout
            pfs.make(name=merlin.merlinFolder, tree=mfs)
        # if it fails
        except OSError as error:
            # complain
            import journal
            return journal.error('merlin.init').log(str(error))

        # mount it
        self.vfs['/project'] = pfs
        self.vfs['/merlin/project'] = pfs[merlin.merlinFolder]

        # if a name was not specified
        if self.project is None:
            # use the last portion of the target folder
            _, self.project = os.path.split(os.path.abspath(folder))

        # build a new project description
        project = merlin.curator.newProject(name=self.project)
        # and save it
        merlin.curator.saveProject(project=project)

        # all done
        return self


    @merlin.export
    def help(self, **kwds):
        """
        Generate the help screen associated with this spell
        """
        # all done
        return


# end of file 
