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
        yield from self.library(library=library, **kwds)
        # all done
        return

    # asset handlers
    @merlin.export
    def library(self, plexus, library, **kwds):
        """
        Generate the workflow that builds a {library}
        """
        # get the library name
        name = library.pyre_name
        # and the renderer
        renderer = self.renderer

        # add  this library to the pile
        yield renderer.commentLine(f"add {library} to the pile of libraries")
        yield f"libraries:: {name}"
        yield ""
        # make a target that builds this library and logs a marker
        yield renderer.commentLine(f"the target that builds {name}")
        yield f"{name}: {name}.assets"
        yield f"\t@$(call log.asset,lib,{name})"
        yield ""

        # prime the asset counters
        counter = {
            "headers": 0,
            "sources": 0,
        }
        # generate some variable definitions
        yield from self._assignments(plexus=plexus, library=library)
        # go through the library assets
        for asset in library.assets:
            # and ask each one to contribute
            yield from asset.identify(
                visitor=self, plexus=plexus, library=library, counter=counter, **kwds
            )
        # generate the build targets
        yield from self._targets(library=library, counter=counter)

        return

    @merlin.export
    def folder(self, folder, library, **kwds):
        """
        Handle a source {folder}
        """
        # assemble the path of the folder relative to the workspace root
        path = library.root / folder.path
        # if the user has marked this folder as one to skip
        if folder.ignore:
            # figure out where the folder got the marker
            where = folder.pyre_where(attribute="ignore")
            # make a channel
            channel = journal.warning("merlin.builder.make")
            # let the user know
            channel.line(f"excluding the folder '{path}'")
            channel.line(f"from the contents of {library}")
            channel.line(f"as explicitly requested")
            channel.line(f"{where}")
            # flush
            channel.log()
            # and move on
            return
        # get the explicit requierements for this folder
        require = folder.require
        # if the folder has explicit dependency requirements that aren't met
        if require and not library.supports(requirements=require):
            # make a channel
            channel = journal.warning("merlin.builder.make")
            # let the user know
            channel.line(f"excluding the folder '{path}'")
            channel.line(f"from the contents of {library}")
            channel.line(f"because its requirements")
            channel.indent()
            channel.report(report=require)
            channel.outdent()
            channel.line(f"could not be satisfied")
            # flush
            channel.log()
            # and move
            return

        # otherwise, get the renderer
        renderer = self.renderer
        # the name of the library
        name = library.pyre_name
        # and its stem
        stem = library.name
        # sign on
        yield renderer.commentLine(f"++ folder: folder")

        # build the path to the clone of the source tree by expanding the corresponding variable
        srcVar = merlin.primitives.path("$(src)") / name / folder.path
        # its vfs equivalent
        srcVFS = merlin.primitives.path("/stage/src") / name / folder.path
        # mark
        yield renderer.commentLine(f"make {srcVFS}")
        # build the dependency line
        yield f"{srcVar}: | {srcVar.parent}"
        # log
        yield f"\t@$(call log.action,mkdir,{srcVFS})"
        # add the rule
        yield f"\t@$(mkdirp) $@"
        # make some room
        yield ""

        # build the directory where the exported headers get installed
        prefixVar = merlin.primitives.path("$(prefix.include)")
        # and the vfs equivalent
        prefixVFS = merlin.primitives.path("/prefix/include")
        # some libraries place their headers within a specific scope
        scope = library.scope
        # if this is the case here
        if scope:
            # make sure it is included in the destination path
            dstVar = prefixVar / scope / stem / folder.path
            # form its vfs equivalent
            dstVFS = prefixVFS / scope / stem / folder.path
        # otherwise
        else:
            # place the headers directly in the include directory
            dstVar = prefixVar / stem / folder.path
            # form its vfs equivalent
            dstVFS = prefixVFS / stem / folder.path
        # mark
        yield renderer.commentLine(f"make {dstVFS}")
        # build the dependency line
        yield f"{dstVar}: | {dstVar.parent}"
        # log
        yield f"\t@$(call log.action,mkdir,{dstVFS})"
        # add the rule
        yield f"\t@$(mkdirp) $@"
        # make some room
        yield ""

        # now, go through the folder contents
        for asset in folder.assets:
            # and ask each one to contribute
            yield from asset.identify(visitor=self, library=library, **kwds)

        # all done
        return

    @merlin.export
    def file(self, file, library, **kwds):
        """
        Handle a {file} asset
        """
        # get the path to the file
        path = library.root / file.path
        # if the user has marked this file as one to skip
        if file.ignore:
            # figure out where the file got the marker
            where = file.pyre_where(attribute="ignore")
            # make a channel
            channel = journal.warning("merlin.builder.make")
            # let the user know
            channel.line(f"excluding the file '{path}'")
            channel.line(f"from the contents of {library}")
            channel.line(f"as explicitly requested")
            channel.line(f"{where}")
            # flush
            channel.log()
            # and move on
            return
        # get the explicit requirements for this file
        require = file.require
        # if the file has explicit dependency requirements that aren't met
        if require and not library.supports(requirements=require):
            # make a channel
            channel = journal.warning("merlin.builder.make")
            # let the user know
            channel.line(f"excluding the file '{path}'")
            channel.line(f"from the contents of {library}")
            channel.line(f"because its requirements")
            channel.indent()
            channel.report(report=require)
            channel.outdent()
            channel.line(f"could not be satisfied")
            # flush
            channel.log()
            # and move
            return
        # get the file category
        category = file.category
        # and ask it to identify itself
        yield from category.identify(visitor=self, library=library, file=file, **kwds)
        # all done
        return

    # asset category handlers
    @merlin.export
    def header(self, library, file, counter, clone=None, **kwds):
        """
        Handle a {header}
        """
        # update the header counter
        counter["headers"] += 1
        # get the renderer
        renderer = self.renderer
        # get the path to the header relative to the library root
        hpath = file.path
        # the library name
        name = library.pyre_name
        # its root
        root = library.root
        # the header scope
        scope = library.scope
        # figure out whether this the gateway header
        gateway = hpath in library.gateway
        # form the path to the source
        src = merlin.primitives.path(f"$({name}.ws)") / hpath
        # form the clone location
        clone = (
            clone
            if clone is not None
            else merlin.primitives.path(f"$({name}.src)") / hpath
        )
        # if this the gateway header
        if gateway:
            # export it to the root of the scope
            prefix = merlin.primitives.path(f"$(prefix.include)") / scope / hpath
        # otherwise
        else:
            # export it within the normal header tree
            prefix = merlin.primitives.path(f"$({name}.include)") / hpath

        # make a tag
        tag = root / hpath
        # mark
        yield renderer.commentLine(f"-- header: {tag}")
        # if this is the gateway header
        if gateway:
            # leave a comment that explains why the rules look different
            yield renderer.commentLine(f"   note: {tag} is a gateway header")
        # mark
        yield renderer.commentLine(f"add {tag} to the pile of exported headers")
        # add it to the exported header pile
        yield from renderer.seti(name=f"{name}.exported", value=f"{prefix}")
        # make some room
        yield ""

        # clone
        yield from self._clone(src=src, clone=clone, tag=tag, **kwds)
        # publish
        yield from self._publish(clone=clone, prefix=prefix, tag=tag, **kwds)

        # all done
        return

    @merlin.export
    def source(self, plexus, library, file, counter, clone=None, language=None, **kwds):
        """
        Handle a {source} file
        """
        # update the source counter
        counter["sources"] += 1
        # get the renderer
        renderer = self.renderer
        # and the host
        host = plexus.pyre_host
        # get the source language
        language = language or file.language.name
        # get the path to the header relative to the library root
        hpath = file.path
        # the library name
        name = library.pyre_name
        # its root
        root = library.root
        # form the path to the source
        src = merlin.primitives.path(f"$({name}.ws)") / hpath
        # form the clone location
        clone = clone or (merlin.primitives.path(f"$({name}.src)") / hpath)
        # build the object module path
        obj = merlin.primitives.path(f"$({name}.build)") / host.object(
            stem="~".join(hpath)
        )
        # make a tag
        tag = root / hpath

        # mark
        yield renderer.commentLine(f"-- {file.language.name} source: {tag}")
        # add the object module to the pile
        yield renderer.commentLine(f"add {obj} to the pile of {name} object modules")
        # adjust the variable
        yield from renderer.seti(name=f"{name}.objects", value=f"{obj}")
        # make some room
        yield ""

        # clone
        yield from self._clone(src=src, clone=clone, tag=tag, **kwds)
        # compiler
        yield from self._compile(
            lib=name, language=language, clone=clone, obj=obj, tag=tag, **kwds
        )

        # all done
        return

    @merlin.export
    def template(self, library, file, **kwds):
        """
        Handle a {template} asset
        """
        return
        # the library name
        name = library.pyre_name
        # the source path
        source = file.path
        # the clone path
        clone = merlin.primitives.path(f"$({name}.src)") / source.parent / source.stem
        # the asset classifier, a dict (suffix -> (category, language))
        classifier = library.languages.classifier
        # classify the target
        category, language = classifier.get(clone.suffix, (None, None))
        # and ask it to identify itself
        yield from category.identify(
            visitor=self,
            library=library,
            file=source,
            clone=clone,
            language=language,
            **kwds,
        )
        # all done
        return

    @merlin.export
    def unrecognizable(self, file, **kwds):
        """
        Handle an {unrecognizable} asset
        """
        # get the renderer
        renderer = self.renderer
        # mark
        yield renderer.commentLine(f" !! unrecognizable: {file.path}")
        # all done
        return

    # source language handlers
    @merlin.export
    def language(self, language, **kwds):
        """
        Handle a source file from an unsupported language
        """
        # get the renderer
        renderer = self.renderer
        # mark
        yield renderer.commentLine(f" !! unknown language {language}")
        # all done
        return

    # helpers
    def _clone(self, src, clone, tag, action="clone", method="$(cp) $< $@", **kwds):
        """
        Stage a workspace file
        """
        # get the renderer
        renderer = self.renderer
        # clone
        yield renderer.commentLine(f"clone {src} to {clone}")
        # add the dependency line
        yield f"{clone}: {src} | {clone.parent}"
        # log
        yield f"\t@$(call log.action,{action},{tag})"
        # the rule
        yield f"\t@{method}"
        # make some room
        yield ""
        # all done
        return

    def _compile(self, lib, language, clone, obj, tag, **kwds):
        """
        Compile a source file
        """
        # get the renderer
        renderer = self.renderer
        # compile
        yield renderer.commentLine(f"compile {clone} to {obj}")
        # make the dependency line
        yield f"{obj}: {clone} | $({lib}.build)"
        # log
        yield f"\t@$(call log.action,{language},{tag})"
        # generate the object module
        yield f"\t@$(call {language}.compile,$<,$@)"
        # make some room
        yield ""

        # all done
        return

    def _publish(self, clone, prefix, tag, **kwds):
        """
        Publish a header file
        """
        # get the renderer
        renderer = self.renderer
        # export
        yield renderer.commentLine(f"export {clone} to {prefix}")
        # add the dependency line
        yield f"{prefix}: {clone} | {prefix.parent}"
        # log
        yield f"\t@$(call log.action,export,{tag})"
        # the rule
        yield f"\t@$(cp) $< $@"
        # make some room
        yield ""

        # all done
        return

    def _assignments(self, plexus, library):
        """
        Generate some library specific variable assignments
        """
        # get the host
        host = plexus.pyre_host
        # get the library name
        name = library.pyre_name
        # its naming stem
        stem = library.name
        # its location within its workspace
        root = library.root
        # and its scope
        scope = library.scope
        # grab the renderer
        renderer = self.renderer

        # form the location of the sources within the workspace
        ws = merlin.primitives.path("$(ws)") / root
        # the location of the cloned source tree
        src = merlin.primitives.path("$(src)") / {name}
        # the location of the build artifacts
        build = merlin.primitives.path("$(build)") / {name}
        # the location of the exported headers
        inc = merlin.primitives.path("$(prefix.include)") / {scope} / {stem}
        # and the location of the archive
        lib = merlin.primitives.path("$(prefix.lib)")

        # the root of the library source tree
        yield renderer.commentLine(f"the location of the {name} sources")
        yield from renderer.set(name=f"{name}.ws", value=f"{ws}")
        # the cloned source
        yield renderer.commentLine(f"the location of the source tree clone")
        yield from renderer.set(name=f"{name}.src", value=f"{src}")
        # the destination of the exported headers
        yield renderer.commentLine(f"the destination of the exported headers")
        yield from renderer.set(name=f"{name}.include", value=f"{inc}")
        # the staging location for the object modules
        yield renderer.commentLine(f"the location of the object modules")
        yield from renderer.set(name=f"{name}.build", value=f"{build}")

        # form the name of the archive
        archive = lib / host.staticLibrary(stem=stem)
        # make a variable for it
        yield renderer.commentLine(f"the {name} archive")
        yield from renderer.set(name=f"{name}.archive", value=f"{archive}")

        # form the name of the dynamic library
        dll = lib / host.dynamicLibrary(stem=stem)
        # make a variable for it
        yield renderer.commentLine(f"the {name} dynamic library")
        yield from renderer.set(name=f"{name}.dll", value=f"{dll}")

        # prime the pile of headers
        yield renderer.commentLine(f"prime the list of exported headers")
        yield from renderer.set(name=f"{name}.exported", value="")
        # and the list of object modules
        yield renderer.commentLine(f"prime the list of object modules")
        yield from renderer.set(name=f"{name}.objects", value="")
        # make some room
        yield ""

        # all done
        return

    def _targets(self, library, counter):
        """
        Build the targets that build the library assets
        """
        # grab the renderer
        renderer = self.renderer
        # get the library name
        name = library.pyre_name

        # if the library has headers
        if counter["headers"]:
            # add the exported headers to the library assets
            yield renderer.commentLine(f"add the exported headers to the {name} assets")
            yield f"{name}.assets:: {name}.headers"
            yield ""
            # export the headers
            yield renderer.commentLine(
                f"publish the target that exports the public headers"
            )
            yield f"{name}.headers: $({name}.exported)"
            yield ""

        # if the library has sources
        if counter["sources"]:
            # realize the build area
            yield renderer.commentLine(f"realize the {name} build area")
            yield f"$(build)/{name}: | $(build)"
            # log
            yield f"\t@$(call log.action,mkdir,/stage/build/{name})"
            # add the rule
            yield f"\t@$(mkdirp) $@"
            yield ""
            # entry point for it
            yield renderer.commentLine(
                f"publish the target that creates the {name} build stage"
            )
            yield f"{name}.build: | $({name}.build)"
            yield ""

            # add the archive to the assets
            yield renderer.commentLine(f"add the static archive to the {name} assets")
            yield f"{name}.assets:: {name}.archive"
            yield ""
            # entry point to build it
            yield renderer.commentLine(
                f"publish the target that builds the {name} archive"
            )
            yield f"{name}.archive: $({name}.archive)"
            yield ""
            # entry point to build its objects
            yield renderer.commentLine(
                f"publish the target that builds the {name} object modules"
            )
            yield f"{name}.objects: $({name}.objects)"
            yield ""

            # build the static library
            yield renderer.commentLine(f"build the static library")
            yield f"$({name}.archive): $({name}.objects) | $(prefix.lib)"
            yield f"\t@$(call log.action,ar,{name}.a)"
            yield f"\t@$(touch) $@"
            yield ""

        # all done
        return


# end of file
