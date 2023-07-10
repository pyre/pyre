# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import merlin

# superclass
from .Fragment import Fragment


# the project builder
class Project(
    Fragment,
    family="merlin.builders.make.project",
    implements=merlin.protocols.flow.project,
):
    """
    Workflow generator for building projects
    """

    # makefile generation
    def generate(self, stage, project, **kwds):
        """
        Generate my makefile
        """
        # build the makefile path
        makefile = stage / "merlin" / project.pyre_name
        # and a comment to be places above the include of my makefile
        marker = f"the '{project.pyre_name}' rules"
        # make some space
        yield ""
        # chain up
        yield from super().generate(
            makefile=makefile, marker=marker, project=project, **kwds
        )
        # all done
        return

    # implementation details
    def _generate(self, project, **kwds):
        """
        Generate my makefile content
        """
        # chain up
        yield from super()._generate(**kwds)
        # render the project makefile
        yield from self.project(project=project)
        # all done
        return

    # asset handlers
    @merlin.export
    def project(self, project, **kwds):
        """
        Generate the workflow that builds a project
        """
        # get the name of the project
        name = project.pyre_name
        # and the renderer
        renderer = self.renderer
        # sign on
        yield renderer.commentLine(f"{name} rules")
        # add this project to the pile
        yield renderer.commentLine(f"add {name} to the pile of projects")
        yield f"projects:: {name}"

        # make a target that builds just this project
        yield ""
        yield renderer.commentLine(f"building {name}")
        # add the libraries to the anchor rule
        yield f"{name}: {name}.assets"
        yield f"\t@$(call log.asset,project,{name})"

        # make a target that builds just this project
        yield ""
        yield renderer.commentLine(f"building {name}")
        # add the libraries to the anchor rule
        yield f"{name}.assets:: {name}.libraries"

        # make some room
        yield ""
        # assemble the library names
        libraries = " ".join(lib.pyre_name for lib in project.libraries)
        # make a variable that holds all the library names
        yield renderer.commentLine(f"the set of {name} libraries")
        yield f"{name}.libraries := {libraries}"
        # and a rule that connects them to the project
        yield renderer.commentLine(f"connect them to the project")
        yield f"{name}.libraries: $({name}.libraries)"

        # all done
        return


# end of file
