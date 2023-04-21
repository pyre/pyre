# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import journal
import merlin

# superclass
from .Fragment import Fragment


# a builder of libraries
class Library(
    Fragment,
    family="merlin.builders.make.lib",
    implements=merlin.protocols.flow.library,
):
    """
    Workflow generator for building libraries
    """

    # interface
    def generate(self, stage, library, **kwds):
        """
        Generate my makefile
        """
        # build the makefile path
        makefile = stage / "merlin" / library.pyre_name
        # and a comment to be places above the include of my makefile
        marker = f"the '{library.pyre_name}' rules"
        # chain up
        yield from super().generate(
            makefile=makefile, marker=marker, library=library, **kwds
        )
        # all done
        return

    # implementation details
    def _generate(self, library, **kwds):
        # chain up
        yield from super()._generate(**kwds)
        # render the library makefile
        yield from self.library(library=library)
        # all done
        return

    # asset handlers
    @merlin.export
    def library(self, library, **kwds):
        """
        Generate the workflow that builds a {library}
        """
        # initialize my asset piles
        folders = []
        headers = []
        sources = []

        # go through the assets of the library
        for asset in library.assets:
            # and add each one to the correct pile
            asset.identify(
                visitor=self,
                library=library,
                folders=folders,
                headers=headers,
                sources=sources,
                **kwds,
            )

        # now, get the name of the library
        name = library.pyre_name
        # and the renderer
        renderer = self.renderer
        # sign on
        yield ""
        yield renderer.commentLine(f"{name} rules")
        # add this library to the pile
        yield renderer.commentLine(f"add {name} to the pile of libraries")
        yield f"libraries:: {name}"

        # make a target that builds just this library
        yield ""
        yield renderer.commentLine(f"building {name}")
        # make the anchor rule
        yield f"{name}: {name}.assets"
        yield f"\t@$(call log.asset,lib,{name})"

        # the directory rules
        yield from self.folderRules(library=library, folders=folders)
        # the asset rules
        yield from self.assetRules(
            library=library, headers=headers, sources=sources, **kwds
        )

        # all done
        return

    @merlin.export
    def folder(self, folder, library, folders, parent=None, **kwds):
        """
        Handle a source {folder}
        """
        # if the user wants to skip this folder
        if folder.ignore:
            # figure out where the folder got marker
            where = folder.pyre_where(attribute="ignore")
            # make a channel
            channel = journal.warning("merlin.builder.make")
            # let the user know
            channel.line(f"excluding folder '{folder.path}'")
            channel.line(f"from the contents of {library}")
            channel.line(f"as explicitly requested")
            channel.line(f"{where}")
            # flush
            channel.log()
            # move on to other things
            return
        # if it has explicit dependency requirements
        if folder.require and not library.supports(requirements=folder.require):
            # skip it
            return
        # otherwise, add it to my pile of folders
        folders.append(folder)
        #  go through its contents
        for asset in folder.assets:
            # and ask each one to identify itself
            asset.identify(
                visitor=self, library=library, parent=folder, folders=folders, **kwds
            )
        # all done
        return

    @merlin.export
    def file(self, file: merlin.assets.file, library: merlin.assets.library, **kwds):
        """
        Handle a {file} asset
        """
        # if the user wants to skip this file
        if file.ignore:
            # move on
            return
        # if it has explicit dependency requirements
        if file.require and not library.supports(requirements=file.require):
            # skip it
            return
        # get the file category
        category = file.category
        # ask it to identify itself
        category.identify(visitor=self, library=library, file=file, **kwds)
        # all done
        return

    # asset category handlers
    @merlin.export
    def header(self, file, headers, **kwds):
        """
        Handle a {header}
        """
        # add the asset to my headers
        headers.append(file)
        # all done
        return

    @merlin.export
    def source(self, file, sources, **kwds):
        """
        Handle a {source} file
        """
        # add the asset to my sources
        sources.append(file)
        # all done
        return

    @merlin.export
    def template(self, **kwds):
        """
        Handle a {template} asset
        """
        # all done
        return

    @merlin.export
    def unrecognizable(self, **kwds):
        """
        Handle an {unrecognizable} asset
        """
        # all done
        return

    # source language handlers
    @merlin.export
    def language(self, **kwds):
        """
        Handle a source file from an unsupported language
        """
        # all done
        return

    # helpers
    def folderRules(self, library, folders):
        """
        Build the rules that construct the prefix directory layout
        """
        # get the name of the library
        name = library.pyre_name
        # the special scope, if any
        scope = library.scope
        # and the renderer
        renderer = self.renderer

        # the common prefix for include directories is stored in a variable
        include = merlin.primitives.path("$(prefix.include)")

        # if the headers are being placed in a special scope
        if scope:
            # the destination includes the scope
            destination = include / scope / library.name
        # otherwise
        else:
            # no scope, just the library name
            destination = include / library.name

        # build the rules that build the individual directories
        yield ""
        yield renderer.commentLine(f"the directory layout of the {name} headers")
        # build the rules
        for dir in folders:
            # compute its destination
            dst = destination / dir.path
            # tag the directory
            tag = f"/prefix/include/{dst.relativeTo(include)}"
            # sign on
            yield ""
            yield renderer.commentLine(f"make {tag}")
            # the dependency line
            yield f"{dst}: | {dst.parent}"
            # log
            yield f"\t@$(call log.action,mkdir,{tag})"
            # the rule
            yield f"\t@$(mkdirp) $@"

        # all done
        return

    def assetRules(self, library, headers, sources, **kwds):
        """
        Build the rules that build {library} assets
        """
        # get the name of the library
        name = library.pyre_name
        # and the renderer
        renderer = self.renderer
        # if there are headers
        if headers:
            # sign on
            yield ""
            yield renderer.commentLine(f"add the headers to the {name} assets")
            yield f"{name}.assets:: {name}.headers"
            # make rules that export the public headers
            yield from self.headerRules(library=library, headers=headers, **kwds)
        # if there are sources
        if sources:
            # add the archive to the library assets
            yield ""
            yield renderer.commentLine(f"add the archive to the {name} assets")
            yield f"{name}.assets:: {name}.archive"
            # make the rules that build the objects
            yield from self.archiveRules(library=library, sources=sources, **kwds)
        # all done
        return

    def headerRules(self, library, headers, **kwds):
        """
        Create a variable that holds all the exported headers
        """
        # get the name of the library
        name = library.pyre_name
        # its root
        root = library.root
        # the special scope, if any
        scope = library.scope
        # the name of the gateway header
        gateway = library.gateway
        # and the renderer
        renderer = self.renderer

        # all exported headers are anchored at
        include = merlin.primitives.path("$(prefix.include)")

        # if the headers are being placed in a special scope
        if scope:
            # the destination includes the scope
            destination = include / scope / library.name
        # otherwise
        else:
            # no scope, just the library name
            destination = include / library.name

        # in order to exclude the gateway
        if gateway:
            # build a sieve
            sieve = lambda x: x.path != gateway
        # and if there isn't one
        else:
            # make it trivial
            sieve = None
        # build the sequence of regular headers
        regular = tuple(filter(sieve, headers))

        # build the variable that holds the regular headers
        # yield ""
        # yield renderer.commentLine(f"the set of {name} headers in the source directories")
        # park the full set of headers in a variable
        # yield from renderer.set(name=f"{name}.headers",
        # multi=(str(header.node.uri) for header in headers))

        # if there is a gateway header
        if gateway:
            # make a tag for it
            tag = root / gateway
            # form its location in the source
            gatewaySrc = "${ws}" / root / gateway
            # its containing folder
            gatewayDir = include / scope
            # and its location in the prefix
            gatewayDst = gatewayDir / gateway

            # build the associated variable
            yield ""
            yield renderer.commentLine(f"the {name} gateway header")
            yield from renderer.set(name=f"{name}.gateway", value=str(gatewayDst))
            # and the rule that copies it
            yield ""
            yield renderer.commentLine(f"publish {tag}")
            # the dependency line
            yield f"{gatewayDst}: {gatewaySrc} | {gatewayDir}"
            # log
            yield f"\t@$(call log.action,cp,{tag})"
            # the rule
            yield f"\t@$(cp) $< $@"
        # otherwise
        else:
            # null the variable so it's not uninitialized
            yield ""
            yield renderer.commentLine(f"{name} doesn't have a gateway header")
            yield from renderer.set(name=f"{name}.gateway", value="")

        # build the variable that holds the exported headers
        yield ""
        yield renderer.commentLine(f"the set of {name} exported headers")
        # make the pile
        yield from renderer.set(
            name=f"{name}.exported",
            multi=(str(destination / header.path) for header in regular),
        )

        # make the aggregator rule that exports headers
        yield ""
        yield renderer.commentLine(f"export the {name} headers")
        yield f"{name}.headers: $({name}.gateway) $({name}.exported)"

        # make the rules that publish individual headers
        for header in regular:
            # the path to the file relative to the workspace root
            hpath = root / header.path
            # sign on
            yield ""
            yield renderer.commentLine(f"publish {hpath}")
            # the dependency line
            yield f"{destination/header.path}: $(ws)/{hpath} | {destination/header.path.parent}"
            # log
            yield f"\t@$(call log.action,cp,{hpath})"
            # the rule
            yield f"\t@$(cp) $< $@"

        # all done
        return

    def archiveRules(self, library, sources, **kwds):
        """
        Build the set of rules that compile the {library} {sources}
        """
        # get the name of the library
        name = library.pyre_name
        # its root
        root = library.root
        # and the renderer
        renderer = self.renderer
        # make a pile of the names of the object files
        objects = tuple(self.formObjectPaths(library, sources))

        # define the macro with the destination archive
        yield ""
        yield renderer.commentLine(f"define the full path to the {name} archive")
        yield from renderer.set(name=f"{name}.archive", value=f"$(prefix.lib)/{name}.a")
        # define the macro with the library staging location
        yield ""
        yield renderer.commentLine(f"define the {name} staging location")
        yield from renderer.set(name=f"{name}.stage", value=f"$(stage)/{name}")
        # define a macro with the archive objects
        yield ""
        yield renderer.commentLine(f"define the set of {name} objects")
        # build the assignment
        yield from renderer.set(name=f"{name}.objects", multi=objects)

        # the archive trigger rule
        yield ""
        yield renderer.commentLine(f"trigger the {name} archive")
        yield f"{name}.archive: $({name}.archive)"
        # the archive build rule
        yield ""
        yield renderer.commentLine(f"make the {name} archive")
        yield f"$({name}.archive): $({name}.objects) | $(prefix.lib)"
        yield f"\t@$(call log.action,ar,{name}.a)"

        # the stage trigger rule
        yield ""
        yield renderer.commentLine(f"trigger the {name} stage")
        yield f"{name}.stage: $({name}.stage)"
        # the stage build rule
        yield ""
        yield renderer.commentLine(f"make the {name} staging location")
        yield f"$({name}.stage):"
        yield f"\t@$(call log.action,mkdir,{name})"
        yield f"\t@$(mkdirp) $@"

        # the object trigger rule
        yield ""
        yield renderer.commentLine(f"trigger the compilation of the {name} sources")
        # make the rule
        yield f"{name}.objects: $({name}.objects)"
        # make the set of rules that compile individual sources
        for src, obj in zip(sources, objects):
            # form the path to the source
            srcp = "${ws}" / root / src.path
            # sign on
            yield ""
            yield renderer.commentLine(f"compile {srcp} to {obj}")
            # make the rule
            yield f"{obj}: {srcp} | $({name}.stage)"
            yield f"\t@$(call log.action,{src.language.name},{root / src.path})"

        # all done
        return

    def formObjectPaths(self, library, sources):
        """
        Build the symbolic path to an object module
        """
        # get the name of the library
        name = library.pyre_name
        # the home of the object modules
        stage = merlin.primitives.path("${stage}") / {name}

        # go through the sources
        for source in sources:
            # hash the filename and add the object extension
            hash = "~".join(source.path) + self.pyre_host.extension_object
            # make it an absolute path
            objpath = stage / hash
            # and make it available
            yield f"{objpath}"

        # all done
        return


# end of file
