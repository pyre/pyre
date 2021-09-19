# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


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

    languages = merlin.properties.tuple(schema=merlin.protocols.language())
    languages.doc = "the languages of the library source assets"


    # interface
    def assets(self):
        """
        Generate the sequence of my source files
        """
        # get the supported languages
        languages = tuple(self.supportedLanguages())
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

        # convert it into an asset
        top = self.directory(name=str(self.root), node=root)
        # starting with my root
        todo = [top]
        # dive into the tree
        for folder in todo:
            # make it available
            yield folder
            # grab its contents
            for node in folder.node.contents.values():
                # form the name of this asset
                name = str(node.uri.relativeTo(ws.uri))
                # folders
                if node.isFolder:
                    # become directories
                    asset = self.directory(name=name, node=node)
                    # and get added to the pile of places to visit
                    todo.append(asset)
                # regular files
                else:
                    # become file based assets
                    asset = self.asset(name=name, node=node)
                    # and get identified
                    self.recognize(asset=asset, languages=languages)
                # either way, assets are attached to their container
                folder.add(asset=asset)
                # and are made available
                yield asset

        # all done
        return


    # implementation details
    def directory(self, name, node):
        """
        Make a new asset container
        """
        # by default, use the raw asset container
        return merlin.assets.directory(name=name, node=node)


    def asset(self, name, node):
        """
        Make a new asset
        """
        # by default, use s raw file asset
        return merlin.assets.file(name=name, node=node)


    def recognize(self, asset, languages):
        """
        Recognize an asset given its filesystem {node} rep
        """
        # if the asset category is already known
        if asset.category:
            # leave it alone
            return

        # if the asset language is known
        if asset.language:
            # override the default suggestions
            languages = [ asset.language ]

        # make a pile of guesses for the asset category
        candidates = []
        # go through the relevant languages
        for language in languages:
            # and ask each one to guess what this is
            guess = language.recognize(asset=asset)
            # if something non-trivial came back
            if guess:
                # add it to the pile
                candidates.append(guess)

        # get the number of candidates
        pop = len(candidates)
        # if there is only one
        if pop == 1:
            # unpack the language and category
            language, category = candidates[0]
            # and mark the asset
            asset.language = language.name
            asset.category = category.category
            # and done
            return

        # if there are no viable candidates
        if pop == 0:
            # mark this as an unrecognizable asset
            asset.category = merlin.assets.unrecognizable.category
            # and done
            return

        # if there are more than one
        for language, candidate in candidates:
            # we require that they are all supporting files
            if not issubclass(candidate, merlin.assets.auxiliary):
                # if any of them fail this constraint assemble the languages that are claiming
                # this asset as their own
                claimants = ", ".join(language.name for language, _ in candidates)
                # make a channel
                channel = journal.warning("merlin.library.assets")
                # complain
                channel.line(f"the file '{asset.pyre_name}'")
                channel.line(f"was claimed by multiple languages: {claimants}")
                channel.line(f"while looking through the assets of '{self.name}'")
                # flush
                channel.log()
                # just in case this error isn't fatal
                return None
        # otherwise, unpack the first one
        _, category = candidates[0]
        # and mark the asset
        asset.category = category.category
        # and done
        return


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

        # if none were specified, fall back to all linkable
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
    def identify(self, authority, **kwds):
        """
        Ask {authority} to process a file based asset
        """
        # attempt to
        try:
            # ask authority for a handler for my type
            handler = authority.library
        # if it doesn't exist
        except AttributeError:
            # chain up
            return super().identify(authority=authority)
        # if it does, invoke it
        return handler(library=self, **kwds)


# end of file
