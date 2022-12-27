# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import journal
import merlin
# superclass
from .Asset import Asset


# class declaration
class Library(Asset,
              family="merlin.assets.libraries.library", implements=merlin.protocols.library):
    """
    A container of binary artifacts
    """


    # user configurable state
    name = merlin.properties.str()
    name.doc = "the name of the library; used as a seed to name its various assets"

    root = merlin.properties.path()
    root.doc = "the path to the library source relative to the root of the repository"

    scope = merlin.properties.path()
    scope.doc = "place my headers within the scope of a larger project"

    gateway = merlin.properties.path()
    gateway.doc = "the name of the top level header that provides access to the other headers"

    languages = merlin.properties.tuple(schema=merlin.protocols.language())
    languages.doc = "the languages of the library source assets"

    # flows
    headers = merlin.properties.set(schema=merlin.protocols.file())
    headers.doc = "the library headers as a set of products in /prefix"


    # interface
    def build(self, builder, **kwds):
        """
        Refresh the library
        """
        # marker
        indent = " " * 2
        # sign on
        print(f"{indent*1}[lib] {self.pyre_name}")
        # go through my headers
        for header in self.headers:
            # ask each one to build itself
            header.build(builder=builder, **kwds)

        # all done
        return super().build(builder=builder, **kwds)


    def assets(self):
        """
        Generate the sequence of my source files
        """
        # get the workspace folder
        ws = self.pyre_fileserver['/workspace']
        # starting with it
        root = ws
        # navigate down to my {root} carefully one step at a time because the filesystem
        # may not have been fully explored by the time we get here
        for folder in self.root.parts:
            # if {root} is empty
            if not root.contents:
                # it probably just requires exploring; gently...
                root.discover(levels=1)
            # if the {folder} is already among the contents of the current directory,
            # someone else has visited and explored this level; mark this folder as
            # the place to explore and move on
            root = root[folder]

        # if we get his far, my {root} exists; all my sources live here
        # so let's explore this subtree
        root.discover()

        # for each asset, there are two interesting projections of its uri:
        # the first one is relative to the project root; we use this to form the asset name
        # because it is guaranteed to be globally unique within a given project; in addition,
        # it is an easily predictable name to use in configuration files
        # the second projection is relative to the root of the library, which gets folded
        # with {/prefix/include} and the library name to locate the installation location of
        # headers, and joined with some special character to form the unique name of the object
        # modules that form an archive

        # for the library {root}, these are trivial: the projection relative to the workspace
        # is its own {root}, by definition
        relWS = self.root
        # and the projection relative to the root is empty
        relLib = merlin.primitives.path()
        # use these to convert the library {root} into an asset and decorate it
        # the name must be a string, so coerce the root projection; these operations are trivial
        # for the library root, but they set the pattern for building all of its assets
        top = self.directory(name=str(relWS / relLib), node=root, path=relLib)
        # and make it available
        yield top

        # build the asset recognizer
        classifier = self.assetClassifier()

        # now, starting with my root
        todo = [top]
        # dive into the tree
        for folder in todo:
            # grab its contents
            for entry, node in folder.node.contents.items():
                # the projection of the asset relative to the library root is given by folding
                # its name onto the projection of its folder
                path = folder.path / entry
                # and the name of this asset is obtained by folding this onto the library root
                name = str(relWS / path)
                # folders
                if node.isFolder:
                    # become directories
                    asset = self.directory(name=name, node=node, path=path)
                    # and get added to the pile of places to visit
                    todo.append(asset)
                # everything else is assumed to be a regular file
                else:
                    # so they become file based assets
                    asset = self.file(name=name, node=node, path=path, classifier=classifier)
                # either way, assets are attached to their container
                folder.add(asset=asset)
                # and are made available
                yield asset

        # all done
        return


    # implementation details
    def directory(self, name, node, path):
        """
        Make a new asset container
        """
        # by default, use the raw asset container
        return merlin.assets.directory(name=name, node=node, path=path)


    def file(self, name, node, path, classifier):
        """
        Make a new asset
        """
        # by default, use the raw file asset
        asset = merlin.assets.file(name=name, node=node, path=path)
        # if the asset is marked as ignored
        if asset.ignore:
            # just leave it alone
            return asset

        # get its configuration
        language = asset.language
        category = asset.category

        # if it already knows its language
        if language:
            # and its category
            if category is not None:
                # nothing further to do
                return asset
            # otherwise, ask the language for help
            asset.category = language.recognize(name=name)
            # and done
            return asset

        # ask the classifier for ideas
        candidate, language = classifier.get(path.suffix, (category, None))
        # if it comes back with a non-trivial answer that contradicts the asset configuration
        if category and candidate is not category:
            # favor what the user supplied, even if it's wrong...
            candidate = category

        # mark
        asset.language = language
        asset.category = candidate

        # all done
        return asset


    def assetClassifier(self):
        """
        Build a table that map file suffixes to asset category and language
        """
        # make a table of suffixes to category and language
        table = merlin.patterns.vivify(levels=2, atom=set)
        # go through the relevant languages
        for language in self.supportedLanguages():
            # go through its suffix categories
            for suffix, category in language.assetClassifier.items():
                # add this to the table
                table[suffix][category].add(language)

        # the cleaned up version of {table} becomes my {assetClassifier}
        assetClassifier = {}
        # go through the table and for each suffix
        for suffix in table:
            # grab the table of candidate categories
            categories = table[suffix]
            # unpack
            category, *conflicts = categories.keys()
            # if there is a conflict
            if conflicts:
                # there is something wrong with the configuration of the supported languages
                channel = journal.firewall("merlin.assets.library")
                # so complain
                channel.line(f"found multiple asset categories for suffix '{suffix}'")
                channel.line(f"candidates:")
                # go through the candidates
                for cat, langs in categories.items():
                    # and show me which languages claim which category
                    channel.line(f"  {cat.category}: from  {', '.join(l.name for l in langs)}")
                # and flush
                channel.log()
                # just in case this firewall is not fatal,
                # set up this suffix as unrecognizable category with no associated language
                assetClassifier[suffix] = "unrecognized", None
                # and move on
                continue
            # now, get the associated languages
            language, *conflicts = categories[category]
            # again, if more than one language compete for this suffix
            if conflicts:
                # the suffix is of unknown language
                language = None
            # mark it
            assetClassifier[suffix] = category, language

        # all done
        return assetClassifier


    def supportedLanguages(self):
        """
        Generate a sequence of the allowed languages
        """
        # grab the set of required languages, as indicated by the user
        languages = self.languages
        # if the user bothered to specify
        if languages:
            # respect the choices
            yield from languages
            # and nothing further
            return

        # if none were specified, fall back to all languages marked {linkable}
        sieve = lambda x: x.linkable
        # supported
        supported = set(
            language for _, _, language in
            merlin.protocols.language.pyre_locateAllImplementers(namespace="merlin")
            )
        # languages
        yield from filter(sieve, supported)

        # all done
        return


    # hooks
    def identify(self, visitor, **kwds):
        """
        Ask {visitor} to process a library
        """
        # attempt to
        try:
            # ask the {visitor} for a handler for my type
            handler = visitor.library
        # if it doesn't exist
        except AttributeError:
            # chain up
            return super().identify(visitor=visitor, **kwds)
        # if it does, invoke it
        return handler(library=self, **kwds)


# end of file
