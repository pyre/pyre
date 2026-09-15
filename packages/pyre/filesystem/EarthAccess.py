# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import time

# support
from .. import primitives

# superclass
from .Filesystem import Filesystem


# the file system factory
class EarthAccess(Filesystem):
    """
    A filesystem built out of the granules that match a query of the NASA common metadata
    repository, as answered by the {earthaccess} package

    The filesystem is the query: its contents are the page of granules the query matches,
    hung on a tree that a {layout} imposes on them. The page is the unit of freshness; a
    discovery at the root re-runs the query, and a discovery anywhere else is answered from the
    page in hand.
    """

    # types
    # the metadata of my leaves
    from .InfoGranule import InfoGranule

    # exceptions
    from .exceptions import DirectoryListingError, SearchError

    # public data
    # the number of granules the catalog reports for my query, as of the last sync
    hits = None

    # interface
    def discover(self, root=None, levels=0, **kwds):
        """
        Fill the tree at {root} with the granules that match my query

        A discovery at the root re-runs the query and rebuilds the whole tree, keeping the nodes
        of the granules that are still on the page and dropping the rest. A discovery at any
        other folder is answered from the page in hand, since the query fetches the page as a
        whole; the page is fetched first if there has never been one.
        """
        # establish the starting point
        root = self if root is None else root
        # if it's not a folder
        if not root.isFolder:
            # complain
            raise self.DirectoryListingError(uri=root.uri, error="not a folder")
        # if the request is for a folder below the root and the page has been fetched before
        if root is not self and self.info(node=self).sync is not None:
            # the page in hand already answers it
            return root
        # otherwise, bring the page current
        self._sync()
        # and hand back the starting point
        return root

    # metamethods
    def __init__(self, query, count=None, layout=None, engine=None, **kwds):
        # the root of the tree is a virtual location
        metadata = self.metadata(uri=primitives.path("/"))
        # chain up
        super().__init__(metadata=metadata, **kwds)
        # save the query parameters
        self.query = dict(query)
        # the cap on the size of the page; {None} fetches every match
        self.count = count
        # the strategy that places a granule on the tree
        self.layout = self.flat if layout is None else layout
        # and the strategy that runs the query
        self.engine = self.cmr if engine is None else engine
        # all done
        return

    # implementation details
    def _sync(self):
        """
        Run my query and rebuild my tree out of the page it answers
        """
        # run the query
        hits, page = self.engine(query=self.query, count=self.count)
        # record the number of matches the catalog reports
        self.hits = hits
        # make a timestamp for this sync
        timestamp = time.gmtime()
        # place every granule on the page at the location the layout picks for it
        live = {primitives.path("/", *self.layout(granule=granule)): granule for granule in page}
        # drop every granule that is no longer on the page
        self._prune(folder=self, live=live)
        # go through the granules on the page
        for path, granule in live.items():
            # build the metadata of the granule
            metadata = self._describe(granule=granule, uri=path, timestamp=timestamp)
            # attempt to
            try:
                # find the node of a granule that survived from the previous page
                node = self._retrieve(uri=path)
            # if it is a newcomer
            except self.NotFoundError:
                # make the folders that lead to it, stamped with this sync
                folder = self._mkfolders(path=path.parent, timestamp=timestamp)
                # make a node for it
                node = folder.node()
                # and hang it on the tree with its metadata
                folder._insert(node=node, uri=primitives.path(path.name), metadata=metadata)
            # if it is a survivor
            else:
                # refresh its metadata, keeping the node itself so that clients that hold on to
                # it see the update
                self.vnodes[node] = metadata
        # stamp my root with the time of this sync
        self.info(node=self).sync = timestamp
        # all done
        return

    def _prune(self, folder, live):
        """
        Drop every granule in {folder} that is not among the {live} paths, and every folder
        that is left empty
        """
        # go through the contents of the folder, on a copy since the contents change
        for name, node in list(folder.contents.items()):
            # if the node is a folder
            if node.isFolder:
                # prune its contents
                self._prune(folder=node, live=live)
                # if anything survived
                if node.contents:
                    # leave it alone
                    continue
            # if the node is a granule that is still on the page
            elif node.uri in live:
                # leave it alone
                continue
            # anything else has vanished; forget its metadata
            del self.vnodes[node]
            # and detach it from its folder
            del folder.contents[name]
        # all done
        return

    def _mkfolders(self, path, timestamp):
        """
        Find or make the folders along {path} and stamp the new ones with {timestamp}
        """
        # start at the root
        folder = self
        # go through the levels of the path
        for name in path.names:
            # look for the folder at this level
            child = folder.contents.get(name)
            # if it is not there
            if child is None:
                # make it
                child = folder.folder()
                # hang it on the tree
                folder[name] = child
                # and stamp it with the time it was made
                self.info(node=child).sync = timestamp
            # descend
            folder = child
        # hand back the folder at the end of the path
        return folder

    def _describe(self, granule, uri, timestamp):
        """
        Build the metadata of {granule} out of its catalog record
        """
        # get the descriptive part of the record
        umm = granule.get("umm", {})
        # the payload description
        payload = umm.get("DataGranule", {})
        # add up the sizes of the files that make up the payload
        size = sum(
            int(entry.get("SizeInBytes", 0))
            for entry in payload.get("ArchiveAndDistributionInformation", [])
        )
        # collect the direct access links
        links = [
            entry["URL"]
            for entry in umm.get("RelatedUrls", [])
            if entry.get("Type") == "GET DATA VIA DIRECT ACCESS"
        ]
        # get the acquisition time range
        window = umm.get("TemporalExtent", {}).get("RangeDateTime", {})
        # build the metadata and return it
        return self.InfoGranule(
            uri=uri,
            sync=timestamp,
            record=granule,
            size=size,
            links=links,
            begin=window.get("BeginningDateTime"),
            end=window.get("EndingDateTime"),
        )

    # the default strategies
    @staticmethod
    def flat(granule):
        """
        Place {granule} at the root of the tree, under its catalog name
        """
        # the catalog name is the leaf name; there are no folders
        return (granule["meta"]["native-id"],)

    @classmethod
    def cmr(cls, query, count):
        """
        Run {query} against the common metadata repository through {earthaccess} and hand back
        the number of matches along with a page of at most {count} of them
        """
        # get the package
        import earthaccess
        from earthaccess.search import DataGranules

        # get the authentication state
        auth = earthaccess.__auth__
        # make a query builder, logged in when the session is
        builder = DataGranules(auth) if auth.authenticated else DataGranules()
        # attempt to
        try:
            # load the query parameters
            search = builder.parameters(**query)
            # count the matches
            hits = search.hits()
            # and fetch the page
            page = search.get(count) if count is not None else search.get_all()
        # if the parameters do not form a query, or the repository is unreachable
        except (ValueError, TypeError, RuntimeError) as error:
            # complain
            raise cls.SearchError(uri=query, error=error)
        # hand back what the catalog said
        return hits, page


# end of file
