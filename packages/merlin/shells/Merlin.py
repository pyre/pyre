# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# external
import journal
import textwrap
# support
import merlin


# declaration
class Merlin(merlin.plexus, family='merlin.shells.plexus'):
    """
    merlin is an opinionated build system that leans on convention to simplify the
    configuration management of complex projects
    """

    # constants
    METAFOLDER = ".merlin"
    # types
    from .Action import Action as pyre_action

    # configurable state
    builder = merlin.protocols.builder()
    builder.doc = "the component that manages the various build products"

    compilers = merlin.properties.tuple(schema=merlin.protocols.compiler())
    compilers.doc = "the list of compilers to use while building projects"

    projects = merlin.properties.tuple(schema=merlin.protocols.project())
    projects.doc = "the list of projects in the current workspace"

    scs = merlin.protocols.scs()
    scs.doc = "the source control system"


    # framework hooks
    # post instantiation hook
    def pyre_initialized(self):
        """
        Go through my traits and force them to materialize
        """
        # give my children their context
        self.builder.merlin_initialized(plexus=self)

        # and indicate that nothing is amiss
        return []


    # virtual filesystem configuration
    def pyre_mountApplicationFolders(self, pfs, prefix, **kwds):
        """
        Explore the application installation folders and construct my private filespace
        """
        # chain up; bypass the rest of the logic here until the UX is enabled
        super().pyre_mountApplicationFolders(pfs=pfs, prefix=prefix, **kwds)

        # N.B: this is early times, so {prefix} may not have been explored; tread carefully

        # grab the fileserver
        vfs = self.vfs
        # find the root of the workspace
        workspacePath = self.pyre_locateParentWith(marker=self.METAFOLDER)
        # if there is one
        if workspacePath:
            # anchor a filesystem on this path
            ws = vfs.retrieveFilesystem(root=workspacePath)
            # grab the metadata directory
            wsmeta = ws[self.METAFOLDER].discover()
            # and, if necessary
            if not self.scs:
                # deduce the source control system
                self.scs = self.deduceSCS(workspace=ws)
        # otherwise
        else:
            # make an empty folder for both the workspace
            ws = vfs.folder()
            # and the meta directory
            wsmeta = pfs.folder()

        # mount the workspace within the global filesystem
        vfs["workspace"] = ws
        # and the metadata directory within my private filesystem
        pfs["workspace"] = wsmeta

        # go no further, for now
        return pfs

        # UX
        # get my namespace
        namespace = self.pyre_namespace
        # look for the web document root, but avoid expanding parts of the local  filesystem
        # that we don't care about and getting trapped in deep directory structures
        # start at the top
        docroot = prefix
        # and descend where we think the main static asset is
        for name in ["etc", namespace, "ux"]:
            # fill the contents of the current node
            docroot.discover(levels=1)
            # attempt to
            try:
                # descend to the next level
                docroot = docroot[name]
            # if not there
            except prefix.NotFoundError:
                # grab a channel
                channel = self.warning
                # complain
                channel.line(f"while looking for UX support:")
                channel.line(f"directory '{docroot.uri}/{name}' not found")
                channel.line(f"disabling the web shell")
                channel.log()
                # mark the UX as unavailable
                self._ux = None
                # and bail
                break
        # if all goes well and we reach the intended folder without errors
        else:
            # instantiate and attach my dispatcher
            self._ux = merlin.ux.dispatcher(plexus=self, docroot=docroot, pfs=pfs)

        # all done
        return pfs


    # instance configuration
    def pyre_loadConfiguration(self, locator):
        """
        Load my configuration files
        """
        # chain up to get files named after me; unlikely to exist while my name continues to
        # be {merlin.plexus}, but whatever...
        super().pyre_loadConfiguration(locator=locator)

        # grab my namespace
        namespace = self.pyre_namespace
        # and my metadata folder
        meta = f"pfs:/workspace"
        # and ask the executive
        executive = self.pyre_executive
        # to load any global configuration files from the workspace metadata folder
        executive.configureStem(stem=namespace, cfgpath=[meta], locator=locator)

        # all done
        return


    # main entry point for the web shell
    def pyre_respond(self, server, request):
        """
        Fulfill an HTTP request
        """
        # get my dispatcher
        ux = self._ux
        # if i don't have one, there is something wrong with my installation
        if ux is None:
            # so everything is an error
            return server.responses.NotFound(server=server)

        # otherwise, ask the dispatcher to do its thing
        return ux.dispatch(plexus=self, server=server, request=request)


    # support for the help system
    def pyre_banner(self):
        """
        Generate the help banner
        """
        # the project header
        yield from textwrap.dedent(merlin.meta.banner).splitlines()
        # the doc string
        yield from self.pyre_showSummary(indent='')
        # the authors
        yield from textwrap.dedent(merlin.meta.authors).splitlines()
        # all done
        return


    # interactive session management
    def pyre_interactiveSessionContext(self, context=None):
        """
        Go interactive
        """
        # prime the execution context
        context = context or {}
        # grant access to my package
        context['merlin'] = merlin  # my package
        # and chain up
        return super().pyre_interactiveSessionContext(context=context)


    # helpers
    def deduceSCS(self, workspace):
        """
        Deduce the source control system
        """
        # start with the common case by looking for a {.git} directory
        if ".git" in workspace:
            # it's git
            return "git"

        # out of ideas
        return None


    # private data
    _ux = None # the UX manager


# end of file
