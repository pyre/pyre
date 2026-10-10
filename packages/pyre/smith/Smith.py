#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import journal
import subprocess

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
        # the templates live with the other platform independent runtime files of the package,
        # under {share/pyre}; every builder puts them there
        return pyre.prefix / "share" / "pyre" / "templates" / self.project.template

    # application obligations
    @pyre.export
    def main(self, *args, **kwds):
        """
        Assemble the project from its template and place it under source control
        """
        # make a channel for reporting progress
        info = journal.info("smith")

        # show me
        info.log(f"template: {self.project}")

        # get the name of the project
        project = self.project.name
        # the templates also want the capitalized name; unless the user chose one
        if self.project.capname is None:
            # derive it from the name
            self.project.capname = project.capitalize()
        # get the nameserver
        nameserver = self.pyre_nameserver
        # make a local filesystem rooted at the model template directory
        template = self.vfs.local(root=self.vault).discover()

        # make a local filesystem rooted at the current directory
        # and explore it carefully
        cwd = self.vfs.local(root=".").discover(levels=1)
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
        info.log("generating the source tree")
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
                # bytecode is not part of a template, but installers that compile every python
                # file they write, e.g. pip, leave it next to the template sources
                if entry == "__pycache__" or entry.endswith(".pyc"):
                    # so leave it behind
                    continue
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
                    body = child.open(mode="rb").read()
                    # and copy it
                    destination = cwd.write(parent=folder, name=entry, contents=body, mode="wb")
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
        info.log("placing the project under source control")
        # make the repository and record the initial revision
        failure = self.placeUnderSourceControl(project=project)
        # if that didn't work out
        if failure is not None:
            # unpack the step that failed and what git had to say about it
            command, message = failure
            # make a channel
            channel = journal.error("smith")
            # the project itself is fine
            channel.line(
                f"the project '{project}' was assembled, but could not be placed under source control"
            )
            # say which step failed
            channel.line(f"while running '{' '.join(command)}':")
            # set git's message apart
            channel.indent()
            # quote it
            channel.report(message)
            # and return to the margin
            channel.outdent()
            # flush
            channel.log()
            # and report failure
            return 1

        # return success
        return 0

    # implementation details
    def placeUnderSourceControl(self, *, project: str) -> tuple[list[str], list[str]] | None:
        """
        Make a git repository in the {project} folder and record its contents as the initial
        revision, tagged 'v0.0.1'; hand back the step that failed and git's account of it, or
        {None} if every step succeeded
        """
        # the steps, in order; each one needs the ones before it
        steps = [
            ["git", "init", "-q", "-b", "main"],
            ["git", "add", "."],
            ["git", "commit", "-q", "-m", "automatically generated source"],
            ["git", "tag", "v0.0.1"],
        ]
        # go through them
        for step in steps:
            # carefully
            try:
                # run this one in the project folder, collecting what git says
                outcome = subprocess.run(step, cwd=project, capture_output=True, text=True)
            # if there is no {git} to run
            except FileNotFoundError as error:
                # hand back the step and the reason
                return step, [str(error)]
            # if the step failed
            if outcome.returncode != 0:
                # hand back the step and git's explanation, wherever git put it
                return step, (outcome.stderr or outcome.stdout).strip().splitlines()
        # all steps succeeded
        return None


# end of file
