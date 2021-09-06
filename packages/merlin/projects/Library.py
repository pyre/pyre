# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# support
import journal
import merlin


# class declaration
class Library(merlin.component,
              family="merlin.projects.libraries.library", implements=merlin.protocols.library):
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
        # grab the set of required languages, as indicated by the user
        languages = self.languages
        # if none were specified
        if not languages:
            # fall back to all linkable
            sieve = lambda x: x.linkable
            # supported
            supported = (lang() for lang in merlin.protocols.language.supported.values())
            # languages
            languages = tuple(filter(sieve, supported))

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

        # starting with my root
        todo = [(root, False)]
        # dive into the tree
        for folder,ignore in todo:
            # form the name of the folder
            name = str(folder.uri.relativeTo(ws.uri))
            # make a directory
            dir = self.directory(name=name, node=folder)
            # if its parent left a marker behind
            if ignore:
                # mark it as well
                dir.ignore = ignore
            # and make it available
            yield dir
            # grab its contents
            for node in folder.contents.values():
                # form the name of this asset
                name = str(node.uri.relativeTo(ws.uri))
                # folders
                if node.isFolder:
                    # get added to the pile of places to visit
                    todo.append((node, dir.ignore))
                    # moving on
                    continue
                # regular files become assets
                asset = self.asset(name=name, node=node)
                # that are attached to their container
                dir.add(asset=asset)
                # identified
                self.recognize(asset=asset, languages=languages)
                # and made available
                yield asset

        # all done
        return


    # implementation details
    def directory(self, name, node):
        """
        Make a new asset container
        """
        # by default, use the raw asset container
        return merlin.projects.directory(name=name, node=node)


    def asset(self, name, node):
        """
        Make a new asset
        """
        # by default, use the raw asset
        return merlin.projects.asset(name=name, node=node)


    def recognize(self, asset, languages):
        """
        Recognize an asset given its filesystem {node} rep
        """
        # make a pile for the asset candidates
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
            # well, that's what it is
            return candidates[0]

        # if there are no viable candidates
        if pop == 0:
            # mark this as an unrecognizable asset
            asset = merlin.projects.unrecognizable(name=name, node=node)
            # and send it off
            return asset

        # if there are more than one
        for candidate in candidates:
            # we require that they are all supporting files
            if not isinstance(candidate, merlin.projects.auxiliary):
                # if any of them fail this constraint assemble the languages that are claiming
                # this asset as their own
                claimants = ", ".join(candidate.language.name for candidate in candidates)
                # make a channel
                channel = journal.error("merlin.library.assets")
                # complain
                channel.line(f"the file '{name}'")
                channel.line(f"was claimed by multiple languages: {claimants}")
                channel.line(f"while looking through the assets of '{self.name}'")
                channel.line(f"")
                # flush
                channel.log()
                # just in case this error isn't fatal
                return None

        # otherwise, just return the first one
        return candidates[0]


# end of file
