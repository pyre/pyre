# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import journal
import merlin


# a builder of libraries
class LibFlow(merlin.component,
              family="merlin.builders.flow.lib", implements=merlin.protocols.libflow):
    """
    Workflow generator for building libraries
    """


    # interface
    # asset handlers
    @merlin.export
    def library(self, renderer, library, **kwds):
        """
        Generate the workflow that builds a {library}
        """
        # initialize my asset piles
        self._directories = []
        self._headers = []
        self._sources = []

        # go through the assets of the library
        for asset in library.assets():
            # and add each one to the correct pile
            asset.identify(visitor=self, renderer=renderer, library=library, **kwds)

        # now, get the name of the library
        name = library.pyre_name
        # sign on
        yield ""
        yield renderer.commentLine(f"building {name}")

        # make the anchor rule
        yield f"{name}: {name}.assets"
        # the directory rules
        yield from self.directoryRules(renderer=renderer,
                                       library=library, directories=self._directories)
        # the asset rules
        yield from self.assetRules(renderer=renderer, library=library, **kwds)

        # all done
        return


    @merlin.export
    def directory(self, directory, **kwds):
        """
        Handle a source {directory}
        """
        # add the asset to my directories
        self._directories.append(directory)
        # all done
        return


    @merlin.export
    def file(self, file, **kwds):
        """
        Handle a {file} asset
        """
        # get the file category
        category = file.category
        # ask it to identify itself
        category.identify(visitor=self, file=file, **kwds)
        # all done
        return


    # asset category handlers
    @merlin.export
    def header(self, file, **kwds):
        """
        Handle a {file} asset
        """
        # add the asset to my headers
        self._headers.append(file)
        # all done
        return


    @merlin.export
    def source(self, file, **kwds):
        """
        Handle a {file} asset
        """
        # add the asset to my sources
        self._sources.append(file)
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


    # metamethods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)

        # initialize my containers
        self._directories = []
        self._headers = []
        self._sources = []

        # all done
        return


    # helpers
    def directoryRules(self, renderer, library, directories):
        """
        Build the rules that construct the prefix directory layout
        """
        # get the name of the library
        name = library.pyre_name
        # the special scope, if any
        scope = library.scope

        # the common prefix for include directories is stored in a variable
        include = merlin.primitives.path("${prefix.include}")

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
        for dir in directories:
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
            yield f"\t@echo [mkdir] {tag}"
            # the rule
            yield f"\t@mkdir -p $@"

        # all done
        return


    def assetRules(self, renderer, library, **kwds):
        """
        Build the rules that build {library} assets
        """
        # unpack
        headers = self._headers
        sources = self._sources
        # get the name of the library
        name = library.pyre_name

        # sign on
        yield ""
        yield renderer.commentLine(f"export the {name} headers")
        yield f"{name}.assets:: {name}.headers"

        # build the header rules
        yield from self.headerRules(renderer=renderer, library=library, headers=headers, **kwds)

        # if there are sources
        if sources:
            # add the archive to the library assets
            yield ""
            yield renderer.commentLine(f"make the {name} archive")
            yield f"{name}.assets:: {name}.archive"
            # make the rules that build the objects
            yield from self.archiveRules(renderer=renderer,
                                         library=library, sources=sources, **kwds)

        # all done
        return


    def headerRules(self, renderer, library, headers, **kwds):
        """
        Create a variable that holds all the exported headers
        """
        # get the name of the library
        name = library.pyre_name
        # its root
        root = library.root
        # the special scope, if any
        scope = library.scope
        # and the name of the gateway header
        gateway = library.gateway

        # all exported headers are anchored at
        include = merlin.primitives.path("${prefix.include}")

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
            yield f"\t@echo [cp] {tag}"
            # the rule
            yield f"\t@cp $< $@"
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
        yield from renderer.set(name=f"{name}.exported",
                                multi=(str(destination / header.path) for header in regular))

        # make the aggregator rule that exports headers
        yield ""
        yield renderer.commentLine(f"export the {name} headers")
        yield f"{name}.headers: ${{{name}.gateway}} ${{{name}.exported}}"

        # make the rules that publish individual headers
        for header in regular:
            # the path to the file relative to the workspace root
            hpath = root / header.path
            # sign on
            yield ""
            yield renderer.commentLine(f"publish {hpath}")
            # the dependency line
            yield f"{destination/header.path}: ${{ws}}/{hpath} | {destination/header.path.parent}"
            # log
            yield f"\t@echo [cp] {hpath}"
            # the rule
            yield f"\t@cp $< $@"

        # all done
        return


    def archiveRules(self, renderer, library, sources, **kwds):
        """
        Build the set of rules that compile the {library} {sources}
        """
        # get the name of the library
        name = library.pyre_name
        # and its root
        root = library.root

        # sign on
        yield ""
        yield renderer.commentLine(f"make the {name} archive")
        # make the rule
        yield f"{name}.archive: {name}.objects"
        yield f"\t@echo [ar] ${{prefix.lib}}/lib{library.name}.a"

        # make a pile of the names of the object files
        objects = tuple(self.formObjectPaths(library, sources))

        # build a variable to hold the archive objects
        yield ""
        yield renderer.commentLine(f"the set of {name} objects")
        # build the assignment
        yield from renderer.set(name=f"{name}.objects", multi=objects)

        # make the aggregator rule for triggering the compilation
        yield ""
        yield renderer.commentLine(f"rule that triggers the compilation of the {name} sources")
        # make the rule
        yield f"{name}.objects: ${{{name}.objects}}"

        # make the set of rules that compile individual sources
        for src, obj in zip(sources, objects):
            # form the path to the source
            srcp = "${ws}" / root / src.path
            # sign on
            yield ""
            yield renderer.commentLine(f"compile {obj} from {srcp}")
            # make the rule
            yield f"{obj}: {srcp}"
            yield f"\t@echo [{src.language.name}] {root / src.path}"

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
            # replace the suffix from the source filename with the object suffix
            stem = source.path.withSuffix(suffix=".o")
            # hash it
            hash = "~".join(stem)
            # make it an absolute path
            objpath = stage / hash
            # and make it available
            yield f"{objpath}"

        # all done
        return


# end of file
