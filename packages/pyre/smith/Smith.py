#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2023 all rights reserved
#


# externals
import journal
import os
# access the framework
import pyre
# my protocols
from .Project import Project


# the application class
class Smith(pyre.application, family="pyre.applications.smith", namespace="smith"):
    """
    A generator of projects in pyre standard form
    """


    # user configurable state
    project = Project()
    project.doc = "the project information"

    force = pyre.properties.bool(default=False)
    force.doc = "overwrite the target directory if it exists"


    # public data
    @property
    def vault(self):
        """
        Return the location of the project template directory
        """
        # build and  return the absolute path to the model template
        return pyre.prefix / 'templates' / self.project.template


    # application obligations
    @pyre.export
    def main(self, *args, **kwds):
        # make a channel for reporting progress
        info = journal.info("smith")

        # get the name of the project
        project = self.project.name
        # get the nameserver
        nameserver = self.pyre_nameserver
        # make a local filesystem rooted at the model template directory
        template = self.vfs.local(root=self.vault).discover()

        # make a local filesystem rooted at the current directory
        # and explore it carefully
        cwd = self.vfs.local(root='.').discover(levels=1)
        # if the target path exists already
        if project in cwd:
            # this is user error
            channel = journal.error("smith")
            # complain
            channel.line(f"the folder '{project}' exists already")
            # flush
            channel.log()
            # and report failure
            return 1

        # show me
        info.log("building the git repository")
        # have {git} create the directory
        os.system(f"git init -q -b main {project}")

        info.log('generating the source tree')
        # initialize the workload
        todo = [(cwd, project, template)]
        # as long as there are folders to visit
        for destination, name, source in todo:
            # show me
            # info.log(f"creating the folder '{name}'")
            # create the new folder
            folder = cwd.mkdir(parent=destination, name=name, exist_ok=True)
            # go through the folder contents
            for entry, child in source.contents.items():
                # attempt to
                try:
                    # expand any macros in the name
                    entry = nameserver.interpolate(expression=entry)
                # if anything goes wrong
                except self.FrameworkError as error:
                    # generate an error message
                    channel = journal.error("smith")
                    # complain
                    channel.line(f"{error}")
                    channel.line(f"while processing '{entry}'")
                    # flush
                    channel.log()
                    # and move on
                    continue
                # show me
                # info.log(f"generating '{entry}'")
                # if the {child} is a folder
                if child.isFolder:
                    # add it to the workload
                    todo.append((folder, entry, child))
                    # and move on
                    continue

                # if the name is blacklisted
                if self.project.blacklisted(filename=entry):
                    # open the file in binary mode and read its contents
                    body = child.open(mode='rb').read()
                    # and copy it
                    destination = cwd.write(parent=folder, name=entry, contents=body, mode='wb')
                # otherwise
                else:
                    # the {child} is a regular file; open it and read its contents
                    body = child.open().read()
                    # attempt to
                    try:
                        # expand any macros
                        body = nameserver.interpolate(expression=body)
                    # if anything goes wrong
                    except (self.FrameworkError, TypeError) as error:
                        # generate an error message
                        channel = journal.error("smith")
                        # complain
                        channel.line(f"{error}")
                        channel.line(f"while processing '{entry}'")
                        # flush
                        channel.log()
                        # and move on
                        continue
                    # create the file
                    destination = cwd.write(parent=folder, name=entry, contents=body)

                # in any case, get me the meta data
                metaold = template.info(child)
                metanew = cwd.info(destination)
                # adjust the permissions of the new file
                metanew.chmod(metaold.permissions)

        # tell me
        info.log('committing the initial revision')
        # build the commit command
        command = [
            "unset CDPATH", # just in case the user has strange tastes
            f"cd {project}",
            "git add .",
            "git commit -q -m 'automatically generated source'",
            "git tag v0.0.1", # tag it
            "cd ..",
            ]
        # execute
        os.system("; ".join(command))

        # return success
        return 0


# end of file
