#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# externals
import os
# access the framework
import pyre
# my protocols
from .Project import Project


# the application class
class Smith(pyre.application, family='pyre.applications.smith'):
    """
    A generator of projects in pyre standard form
    """


    # user configurable state
    project = Project()
    project.doc = "the project information"


    # public data
    @property
    def vault(self):
        """
        Return the location of the project template directory
        """
        # build and  return the absolute path to the model template
        return os.path.join(pyre.prefix, 'templates', self.project.template)


    # application obligations
    @pyre.export
    def main(self, *args, **kwds):
        # get the name of the project
        project = self.project.name
        # instantiate my host configuration so that its settings materialize
        host = self.project.live
        # get the nameserver
        nameserver = self.pyre_nameserver
        # make local filesystem rooted at the model template directory
        template = self.vfs.local(root=self.vault).discover()

        # if the target path exists already
        if os.path.exists(project):
            # complain
            self.error.log("the folder {!r} exists already".format(project))
            # report failure
            return 1

        # make a local filesystem rooted at the current directory
        cwd = self.vfs.local(root='.')

        # initialize the workload
        todo = [(cwd, project, template)]
        # as long as there are folders to visit
        for destination, name, source in todo:
            # show me
            self.info.log('creating the folder {!r}'.format(name))
            # create the new folder
            folder = cwd.mkdir(parent=destination, name=name)
            # go through the folder contents
            for entry, node in source.contents.items():
                # expand any macros in the name
                entry = nameserver.interpolate(expression=entry)
                # show me
                self.info.log('generating {!r}'.format(entry))
                # if the {node} is a folder
                if node.isFolder:
                    # add it to the workload
                    todo.append((folder, entry, node))
                    # and move on
                    continue
                # otherwise, the {node} is a regular file; open it
                with node.open() as raw:
                    # pull the contents
                    body = raw.read()
                    # expand any macros
                    body = nameserver.interpolate(expression=body)
                    # create the file
                    destination = cwd.write(parent=folder, name=entry, contents=body)
                    # get me the meta data
                    metaold = template.info(node)
                    metanew = cwd.info(destination)
                    # adjust the permissions of the new file
                    metanew.chmod(metaold.permissions)

        # return success
        return 0


# end of file
