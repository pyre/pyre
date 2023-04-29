# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2023 all rights reserved
#


# externals
import journal
import hashlib
import mmap
import time

# superclass
from .Filesystem import Filesystem


# class declaration
class Local(Filesystem):
    """
    An encapsulation of a filesystem mounted directly on the local host machine
    """

    # exceptions
    from .exceptions import DirectoryListingError, URISpecificationError

    # public data
    walker = None  # the directory listing mechanism
    recognizer = None  # the file type recognizer

    # interface
    def checksum(self, node, **kwds):
        """
        Compute a checksum for the node
        """
        # open the file
        with self.open(node, mode="rb") as stream:
            # get the file contents
            contents = mmap.mmap(stream.fileno(), length=0, access=mmap.ACCESS_READ)
            # pull the contents
            return hashlib.sha256(contents).digest()
        # if anything goes wrong, do something stupid
        return 0

    def open(self, node, **kwds):
        """
        Open the file associated with {node}
        """
        # get the info record associated with the node and extract the file uri
        uri = self.vnodes[node].uri
        # attempt to
        try:
            # call the system {open} and return the result
            return uri.open(**kwds)
        # if this fails
        except OSError as error:
            # complain
            raise self.URISpecificationError(uri=uri, reason=str(error))

    def mkdir(self, name, parent=None, **kwds):
        """
        Create a subdirectory {name} in {parent}
        """
        # maybe it's all about me after all
        if parent is None:
            parent = self
        # assemble the new folder uri
        uri = parent.uri / name
        # create the directory
        uri.mkdir(**kwds)
        # if we get this far, the directory has been created; update my internal structure
        folder = parent.folder()
        # insert the new node in its parent's contents
        parent[name] = folder
        # and return the new folder
        return folder

    def touch(self, name, parent=None, **kwds):
        """
        Create a file {name} in directory {parent}
        """
        # maybe it's all about me after all
        if parent is None:
            parent = self
        # assemble the new node uri
        uri = parent.uri / name
        # create the file
        uri.open(mode="w").close()
        # if we get this far, the file has been created; update my internal structure
        node = parent.node()
        # insert the new node in its parent's contents
        parent.contents[str(name)] = node
        # get the directory meta-data
        meta = self.recognizer.recognize(uri)
        # and update my {vnode} table
        self.vnodes[node] = meta
        # all done
        return node

    def write(self, name, contents, parent=None, mode="w"):
        """
        Create the file {name} in the folder {parent} with the given {contents}
        """
        # maybe it's all about me after all
        if parent is None:
            parent = self
        # assemble the new file uri
        uri = parent.uri / name
        # create the file
        with uri.open(mode=mode) as file:
            # save its contents
            file.write(contents)
        # build a node
        node = parent.node()
        # insert the new node in its parent's contents
        parent.contents[name] = node
        # get the file meta-data
        meta = self.recognizer.recognize(uri)
        # and update my {vnode} table
        self.vnodes[node] = meta
        # all done
        return node

    def make(self, name, tree, root=None, **kwds):
        """
        Duplicate the hierarchical structure in {tree} within my context
        """
        # print(" ** pyre.filesystem.Local.make:")
        # create a timestamp
        timestamp = time.gmtime()
        # adjust the location of the new branch
        root = self if root is None else root
        # print(" ++ input:")
        # print("      root: {}".format(root))
        # print("      uri: {!r}".format(root.uri))
        # print("      tree: {!r}".format(tree.uri))

        # initialize the worklist
        todo = [(root, name, tree)]
        # print(" ++ adding:")
        # as long as there is more to do
        for parent, name, source in todo:
            # create the directory
            folder = self.mkdir(parent=parent, name=name, exist_ok=True)
            # add the children to my work list
            todo.extend(
                (folder, name, child)
                for name, child in source.contents.items()
                # NYI: don't know how to handle regular files just yet; must take into account
                # the meta data associated with {node} in whatever filesystem {tree} came from,
                # just in case I am ever asked to build pipes and sockets and stuff... skip for
                # now.
                if child.isFolder
            )

        return tree

    def unlink(self, node, **kwds):
        """
        Remove {node} and its associated file from this filesystem
        """
        # ask the path to delete itself
        node.uri.unlink()
        # remove the node from my vnode table
        del self.vnodes[node]
        # all done here; the parent folder will take care of updating its contents
        return

    def discover(self, root=None, walker=None, recognizer=None, levels=None, **kwds):
        """
        Traverse the local filesystem starting with {root} and refresh my contents so that they
        match the underlying filesystem
        """
        # deduce the filesystem to which {root} belongs
        fs = root.filesystem() if root is not None else self
        # if it is not one of my nodes
        if fs is not self:
            # ask the other guy to do the work
            return fs.discover(
                root=root, walker=walker, recognizer=recognizer, levels=levels, **kwds
            )

        # create a timestamp so we know the last time the filesystem contents were refreshed
        timestamp = time.gmtime()
        # use the supplied traversal support, if available; otherwise, use mine
        walker = self.walker if walker is None else walker
        recognizer = self.recognizer if recognizer is None else recognizer

        # establish the starting point
        root = self if root is None else root
        # and make sure it is is a folder
        if not root.isFolder:
            # otherwise complain
            raise self.DirectoryListingError(uri=root.uri, error="not a directory")

        # show me where we are
        # print(f" ** pyre.filesystem.Local")
        # print(f"  input:")
        # print(f"    root: '{root}'")
        # print(f"    root uri: '{root.uri}'")
        # print(f"    levels: {levels}")
        # and mark the beginning of discovery
        # print(f"  visiting:")

        # initialize the traversal: pairs made of the node we are working on, and the depth of
        # the traversal at the level of this node
        todo = [(root, 0)]
        # start walking and recognizing
        for folder, level in todo:
            # if we have gotten deeper than the user requested
            if levels is not None and level >= levels:
                # do something else
                continue
            # compute the actual location of this folder
            location = self.vnodes[folder].uri
            # show me
            # print(f"    uri: {location}")
            # put the current contents of the folder on a pile; once we recognize the actual
            # contents of the folder, we will remove them from this pile; what's left are
            # entries that disappeared since the last time we walked the folder and must be
            # removed
            dead = set(folder.contents)
            # show me
            # print(f"    contents: {dead}")
            # walk through the contents
            for entry in walker.walk(location):
                # show me
                # print(f"      {entry}")
                # ask the recognizer for the entry type
                meta = recognizer.recognize(entry)
                # if the recognizer failed
                if not meta:
                    # attempt to
                    try:
                        # make a channel
                        channel = journal.debug("pyre.filesystem.discover")
                    # if it fails
                    except AttributeError:
                        # it's just too early in the bootstrapping process to involve the user
                        pass
                    # if we have journal
                    else:
                        # leave a note
                        channel.line(f"unable to determine the type of '{entry}'")
                        channel.line(f"while exploring '{location}'")
                        channel.log()
                    # in wither case, just ignore this entry
                    continue
                # stamp the entry meta-data
                meta.syncTime = timestamp
                # get the entry name
                name = entry.name
                # remove from the pile of dead entries
                dead.discard(name)
                # attempt to
                try:
                    # get the node associated with {name} in this {folder}
                    node = folder[name]
                # if the node doesn't exist, either we are exploring this tree for the first time
                # or the {entry} was created since the last time we visited; in any case
                except self.NotFoundError:
                    # build a new one
                    node = folder.folder() if meta.isFolder else folder.node()
                    # if we are building a folder
                    if meta.isFolder:
                        # make it
                        node = folder.folder()
                        # and add its location to our {todo} pile so we can visit it as well
                        todo.append((node, level + 1))
                    # otherwise
                    else:
                        # make a regular node
                        node = folder.node()
                    # attach the new node to its folder
                    folder[name] = node
                # new or old, update the metadata of the node; we do this for old nodes as well
                # because we keep track of the last time the folder was explored
                self.vnodes[node] = meta
                # and if the current node is a folder
                if meta.isFolder:
                    # add it to our {todo} pile
                    todo.append((node, level + 1))

            # we are done with this folder; show me the dead nodes
            # print(f"    dead: {dead}")
            # go through them
            for entry in dead:
                # remove them from the table of {vnodes}
                del self.vnodes[folder[entry]]
                # and from the folder contents
                del folder.contents[entry]

        # show me
        # print(f"    after uri: '{self.vnodes[root].uri}'")
        # all done
        return root

    # meta methods
    def __init__(self, walker, recognizer, **kwds):
        # chain up
        super().__init__(**kwds)
        # attach the default content discovery mechanisms
        self.walker = walker
        self.recognizer = recognizer
        # all done
        return


# end of file
