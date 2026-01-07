# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre
import journal

# external
import time
from botocore.exceptions import BotoCoreError, ClientError

# superclass
from .Filesystem import Filesystem


# the file system factory
class S3(Filesystem):
    """
    A filesystem built out of the contents of an S3 bucket
    """

    # exceptions
    from .exceptions import DirectoryListingError

    # fill {root} with the content
    def discover(self, root=None, levels=0, **kwds):
        """
        Retrieve the contents at {root} from my S3 bucket
        """
        # establish the starting point
        root = self if root is None else root
        # and if it's not a folder
        if not root.isFolder:
            # complain
            raise self.DirectoryListingError(uri=root.uri, error="not a directory")

        # set the search delimiter
        delimiter = "/"
        # make an S3 client and ask it for a  paginator
        paginator = self.session.client("s3").get_paginator("list_objects_v2")
        # prime the workload; we'll add subdirectories here as we discover them
        todo = [(root, 0)]
        # start walking the bucket contents
        for folder, level in todo:
            # check whether we are deeper in the bucket than the user limit
            if levels is not None and level >= levels:
                # move on
                continue
            # place the current contents of folder in a pile; we will use this to detect which nodes
            # have been removed since the last time we synced with the s3 bucket so we can clean
            # them up
            dead = set(folder.contents)
            # get the location of this folder
            here = self.info(node=folder).uri
            # extract its prefix; aws needs a string with no leading '/"
            prefix = delimiter.join(here.address[1:])
            # if it's not properly terminated
            if not prefix.endswith(delimiter):
                # force it
                prefix += delimiter

            # while the paginator is able to retrieve more content, ask for it; set the {delimiter}
            # to "/" to ask it to stop fetching entries at the next occurrence of the {delimiter},
            # effectively limiting the search to what we are going to interpret as the contents of a
            # directory; it is also very important to terminate the {prefix} with the {delimiter} so
            # that we find the next one, rather than short circuiting the search to the current
            # level
            opts = {
                # set the bucket; it's in the {authority} field of the current location
                "Bucket": here.authority,
                # make sure the {prefix} is {delimiter} terminated and add it to the pile
                "Prefix": prefix,
                # and truncate key names to the next occurrence of the {delimiter}
                "Delimiter": delimiter,
            }
            # go through the pages
            for page in paginator.paginate(**opts):
                # process the page contents
                self._processPage(
                    folder=folder,
                    here=here,
                    level=level,
                    dead=dead,
                    page=page,
                    todo=todo,
                )
            # now, go through the nodes that are still in the dead pile
            for name in dead:
                # ask {folder} for the node that corresponds to the name
                node = folder[name]
                # remove the node from my {vnode} table
                del self.vnodes[node]
                # and from the folder
                del folder.contents[name]
        # all done
        return root

    # metamethods
    def __init__(self, session, root, **kwds):
        # for the {address} of {root} to be a path, until pyre.primitives.uri does...
        root = root.clone(address=pyre.primitives.path(root.address))
        # build my metadata
        metadata = self.metadata(uri=root)
        # and chain up
        super().__init__(metadata=metadata, **kwds)
        # save the s3 connection
        self.session = session
        # all done
        return

    # implementation details
    def _processPage(self, folder, here, level, dead, page, todo):
        """
        Process one page of bucket contents
        """
        # make a timestamp
        timestamp = time.gmtime()
        # get the items that are stored at this prefix
        items = [entry["Key"] for entry in page.get("Contents", [])]
        # go through the items
        for entry in items:
            # build nodes for them
            node = folder.node()
            # assemble the path to the entry
            loc = pyre.primitives.path.root / entry
            # form the name by which they are known to their container
            name = loc.name
            # connect the pair to the folder we are visiting
            folder[name] = node
            # get the metadata of the new {node}
            meta = self.info(node)
            # so we can mark the time of last sync
            meta.sync = timestamp
            # and remove this node from the {dead} pile, if it's there
            dead.discard(name)

        # now, extract the prefixes to the rest of the bucket contents, given our delimiter
        # these will become folders in the s3 filesystem
        prefixes = [entry["Prefix"] for entry in page.get("CommonPrefixes", [])]
        # go through the prefixes
        for entry in prefixes:
            # these will be folders
            node = folder.folder()
            # assemble the path to the entry
            loc = pyre.primitives.path.root / entry
            # form the name by which they are known to their container
            name = loc.name
            # and connect them to the folder we are visiting
            folder[name] = node
            # get the metadata of the new {node}
            meta = self.info(node)
            # so we can mark the time of last sync
            meta.sync = timestamp
            # also, add them to the to-do pile along with a level marker so we can
            # visit them to get their contents
            todo.append((node, level + 1))
            # finally, remove them from the {dead} pile
            dead.discard(name)

        # all done
        return


# end of file
