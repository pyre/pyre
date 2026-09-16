# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import copy
import io
import os

# support
from ... import primitives


# the round trip editor
class Editor:
    """
    An editor of yaml documents that leaves everything it does not touch as it found it

    The document is edited by key path, never regenerated: comments, blank lines, quoting, and
    the flow style of the entries the editor does not touch survive the trip through it. The
    editor rides on {ruamel.yaml}; when that package is not importable, the editor reports
    itself unavailable and raises {MissingBackendError} when built
    """

    # exceptions
    from ..exceptions import EditingError, MissingBackendError

    # interface
    @classmethod
    def available(cls):
        """
        Check whether the backend is importable
        """
        # attempt to
        try:
            # get the backend
            import ruamel.yaml
        # if it is not there
        except ImportError:
            # say so
            return False
        # otherwise, all is well
        return True

    def get(self, *path, default=None):
        """
        Retrieve the value at {path}, or {default} when the document has nothing there
        """
        # start at the top
        node = self.document
        # go through the keys
        for key in path:
            # a scalar or a missing key ends the search
            if not isinstance(node, (self.Map, self.Seq)) or not self._holds(node=node, key=key):
                # with the default
                return default
            # descend
            node = node[key]
        # hand off whatever was found
        return node

    def set(self, *path, value):
        """
        Store {value} at {path}, making the mappings that lead to it as necessary
        """
        # the path must name something
        if not path:
            # otherwise complain
            raise self.EditingError(codec=self, reason="an empty path names nothing")
        # find the container, making the mappings along the way
        container = self._reach(path=path[:-1])
        # and the key
        key = path[-1]
        # convert the value into a form that keeps comments
        value = self._adopt(value=value)
        # if the key is already there
        if self._holds(node=container, key=key):
            # the trailing comment of its old value, if any, must survive the replacement
            token = self._take(node=container[key])
            # replace the value
            container[key] = value
            # and give the comment to the new value
            self._give(node=value, token=token, fallback=(container, key))
            # all done
            return self
        # otherwise, the entry goes at the end of the container; the comment block that trails
        # the current tail, or the one held for the container while it was empty, belongs
        # after the new entry; a new top level section is set apart from the one before it by
        # the blank lines that opened the block, which stay behind
        tail, _ = self._tail(node=container)
        residue = container is self.document and tail is not container
        token = self._take(node=container, residue=residue) or self._release(node=container)
        # add the entry
        container[key] = value
        # and place the comment after it
        self._give(node=value, token=token, fallback=(container, key))
        # all done
        return self

    def delete(self, *path):
        """
        Remove the entry at {path}, reporting whether it was there
        """
        # the path must name something
        if not path:
            # otherwise complain
            raise self.EditingError(codec=self, reason="an empty path names nothing")
        # find the container
        container = self.get(*path[:-1])
        # and the key
        key = path[-1]
        # if there is no such entry
        if not isinstance(container, (self.Map, self.Seq)) or not self._holds(container, key):
            # say so
            return False
        # the comment block that trails the entry must survive its removal
        token = self._take(node=container[key])
        # the block that precedes the entry as well
        preamble = self._takePreamble(container=container, key=key)
        # remove the entry
        del container[key]
        # and settle the comments on the new tail of the container
        self._settle(container=container, token=token, preamble=preamble)
        # all done
        return True

    def append(self, *path, value):
        """
        Add {value} to the end of the list at {path}, making the list as necessary
        """
        # look for the list
        target = self.get(*path)
        # if there is nothing there
        if target is None:
            # make an empty list
            self.set(*path, value=[])
            # and get it
            target = self.get(*path)
        # anything but a list is a mistake
        if not isinstance(target, self.Seq):
            # so complain
            raise self.EditingError(codec=self, reason=f"the entry at {path} is not a list")
        # convert the value into a form that keeps comments
        value = self._adopt(value=value)
        # the comment block that trails the current tail, or the one held for the list while
        # it was empty, belongs after the new item
        token = self._take(node=target) or self._release(node=target)
        # add the item
        target.append(value)
        # and place the comment after it
        self._give(node=value, token=token, fallback=(target, len(target) - 1))
        # all done
        return self

    def remove(self, *path, value):
        """
        Remove {value} from the list at {path}, reporting whether it was there
        """
        # look for the list
        target = self.get(*path)
        # if there is no list there
        if not isinstance(target, self.Seq):
            # there is nothing to remove
            return False
        # go through the items
        for index, item in enumerate(target):
            # looking for the value
            if item == value:
                # remove it, along with any comments it carries
                return self.delete(*path, index)
        # not there
        return False

    def render(self):
        """
        Build the text of the document
        """
        # comments held for containers that never got an entry go where they were headed
        for fallback, token in self._held.values():
            # unpack the fallback
            container, key = fallback
            # and place the token there
            self._slot(container=container, key=key)[self._position(container=container)] = token
        # nothing is held any more
        self._held.clear()
        # make a buffer
        buffer = io.StringIO()
        # dump the document into it
        self.backend.dump(self.document, buffer)
        # and hand off the text
        return buffer.getvalue()

    def save(self, uri=None):
        """
        Write the document back to {uri}, or to where it was read from, all at once
        """
        # resolve the target
        uri = self.uri if uri is None else primitives.path(uri)
        # a document without a location has nowhere to go
        if uri is None:
            # so complain
            raise self.EditingError(codec=self, reason="the document has no location")
        # write the text next to the target
        scratch = uri.parent / f".{uri.name}.editing"
        # carefully
        with scratch.open(mode="w", encoding="utf-8") as stream:
            # write
            stream.write(self.render())
        # and move it into place, so readers never see a partial document
        os.replace(str(scratch), str(uri))
        # remember the location
        self.uri = uri
        # all done
        return self

    # metamethods
    def __init__(self, uri=None, text=None, **kwds):
        # chain up
        super().__init__(**kwds)
        # if the backend is not there
        if not self.available():
            # complain
            raise self.MissingBackendError(codec=self, uri=uri, package="ruamel.yaml")
        # get the backend
        from ruamel.yaml import YAML
        from ruamel.yaml.comments import CommentedMap, CommentedSeq

        # the container types the backend uses to keep comments
        self.Map = CommentedMap
        self.Seq = CommentedSeq
        # build the backend, in round trip mode
        backend = YAML(typ="rt")
        # keep the quoting of the original
        backend.preserve_quotes = True
        # and lay out new entries the way pyre configuration files are indented
        backend.indent(mapping=4, sequence=4, offset=4)
        # save it
        self.backend = backend
        # normalize the location
        self.uri = None if uri is None else primitives.path(uri)
        # if text was given, it is the document
        if text is None and self.uri is not None and self.uri.exists():
            # otherwise, read the file
            text = self.uri.open(mode="r", encoding="utf-8").read()
        # parse the text, or start from an empty document
        document = backend.load(text) if text else None
        # an empty document is an empty mapping
        self.document = CommentedMap() if document is None else document
        # the comments held for containers that are still empty, keyed by container identity
        self._held = {}
        # all done
        return

    # implementation details
    def _holds(self, node, key):
        """
        Check whether {node} has an entry at {key}
        """
        # a list holds an index within its range
        if isinstance(node, self.Seq):
            # so check
            return isinstance(key, int) and -len(node) <= key < len(node)
        # a mapping holds its keys
        return key in node

    def _reach(self, path):
        """
        Find the mapping at {path}, making the mappings along the way as necessary
        """
        # start at the top
        node = self.document
        # go through the keys
        for key in path:
            # if the key is missing
            if not self._holds(node=node, key=key):
                # make a mapping for it, placing the trailing comment of the container after it
                self.set(*path[: path.index(key) + 1], value=self.Map())
            # descend
            node = node[key]
            # anything but a mapping cannot hold keys
            if not isinstance(node, self.Map):
                # so complain
                raise self.EditingError(codec=self, reason=f"the entry at {key!r} is not a mapping")
        # hand off the mapping
        return node

    def _adopt(self, value):
        """
        Convert {value} into the backend's containers, so comments can be attached to it
        """
        # tables
        if isinstance(value, dict):
            # become mappings, entry by entry
            return self.Map((key, self._adopt(value=item)) for key, item in value.items())
        # sequences
        if isinstance(value, (list, tuple)):
            # become lists, item by item
            return self.Seq(self._adopt(value=item) for item in value)
        # everything else travels as it is
        return value

    def _tail(self, node):
        """
        Find the container and key of the deepest last entry of {node}
        """
        # nothing yet
        container, key = None, None
        # start with the node
        current = node
        # descend
        while True:
            # a non-empty mapping continues with its last key
            if isinstance(current, self.Map) and len(current):
                # get it
                key = list(current.keys())[-1]
            # a non-empty list continues with its last item
            elif isinstance(current, self.Seq) and len(current):
                # get it
                key = len(current) - 1
            # a scalar or an empty container is the end
            else:
                # hand off what was reached
                return container, key
            # remember the container
            container = current
            # and descend
            current = current[key]

    def _slot(self, container, key):
        """
        Get the comment record of {key} in {container}, making an empty one if necessary
        """
        # the backend keeps four positions per entry
        return container.ca.items.setdefault(key, [None, None, None, None])

    def _position(self, container):
        """
        The position of the trailing comment in the comment record of an entry of {container}
        """
        # lists keep it first, mappings third
        return 0 if isinstance(container, self.Seq) else 2

    def _take(self, node, residue=False):
        """
        Detach and return the comment block that trails the deepest last entry of {node}

        With {residue} set, the blank lines that open the block stay behind, to set the old
        tail apart from the new top level section about to follow it
        """
        # find the tail
        container, key = self._tail(node=node)
        # a node without entries has no trailing comment
        if container is None:
            # so there is nothing to take
            return None
        # get the record
        slot = container.ca.items.get(key)
        # if there is none
        if slot is None:
            # there is nothing to take
            return None
        # get the position
        position = self._position(container=container)
        # take the token
        token = slot[position]
        # if there is none
        if token is None:
            # there is nothing to take
            return None
        # the blank lines that open the block separate the old tail from whatever follows it;
        # the block itself moves, blank lines and all
        text = token.value
        # count the newlines that open it, past the one that ends the line of the value
        blanks = len(text) - len(text.lstrip("\n"))
        # if the blank lines are wanted and there are any
        if residue and blanks > 1:
            # leave a copy of them behind
            residue = copy.copy(token)
            residue.value = "\n" * blanks
            slot[position] = residue
        # otherwise
        else:
            # clear the slot
            slot[position] = None
        # and hand off the token
        return token

    def _give(self, node, token, fallback):
        """
        Attach {token} after the deepest last entry of {node}, or at {fallback}, a container
        and key, when {node} has no entries
        """
        # nothing to place
        if token is None:
            # is nothing to do
            return
        # an empty container cannot carry the comment yet: attached to its key, the comment
        # would render between the key and the entries that come later; hold it until the
        # first entry arrives, remembering where it goes if none ever does
        if isinstance(node, (self.Map, self.Seq)) and not len(node):
            # hold it
            self._held[id(node)] = (fallback, token)
            # all done
            return
        # find the tail
        container, key = self._tail(node=node)
        # a scalar takes the comment at the fallback
        if container is None:
            # unpack it
            container, key = fallback
        # place the token
        self._slot(container=container, key=key)[self._position(container=container)] = token
        # all done
        return

    def _release(self, node):
        """
        Hand back the comment held for {node} while it was empty, if any
        """
        # look it up, forgetting it
        held = self._held.pop(id(node), None)
        # and hand back the token
        return None if held is None else held[1]

    def _takePreamble(self, container, key):
        """
        Detach and return the comment lines that precede {key} in {container}
        """
        # lists have no preambles
        if isinstance(container, self.Seq):
            # so there is nothing to take
            return None
        # get the record
        slot = container.ca.items.get(key)
        # if there is none
        if slot is None:
            # there is nothing to take
            return None
        # the preamble sits last
        preamble = slot[3]
        # clear it
        slot[3] = None
        # and hand it off
        return preamble

    def _settle(self, container, token, preamble):
        """
        Place the comments that were attached to a removed entry of {container}
        """
        # the trailing block goes after the new tail of the container
        if token is not None:
            # find it
            tail, key = self._tail(node=container)
            # if the container still has entries
            if tail is not None:
                # the block goes there, after whatever trails the new tail
                self._append(container=tail, key=key, token=token)
            # otherwise
            else:
                # the block is attached to the container's own trailing comment, at the top
                self._orphan(token=token)
        # the preamble goes before the next entry, which is now at the same position; with the
        # removed entry gone from the end of a mapping, the lines join the trailing block
        if preamble:
            # find the tail
            tail, key = self._tail(node=container)
            # if the container has entries
            if tail is not None:
                # fold the lines into the trailing comment
                self._append(container=tail, key=key, token=self._join(preamble))
            # otherwise
            else:
                # keep them at the top
                self._orphan(token=self._join(preamble))
        # all done
        return

    def _append(self, container, key, token):
        """
        Add {token} after whatever already trails {key} in {container}
        """
        # get the record and the position
        slot = self._slot(container=container, key=key)
        position = self._position(container=container)
        # if nothing trails the entry
        if slot[position] is None:
            # the token does
            slot[position] = token
            # all done
            return
        # otherwise, join the texts
        slot[position].value = slot[position].value + token.value
        # all done
        return

    def _orphan(self, token):
        """
        Keep {token}, a comment that lost its entry, at the top of the document
        """
        # the document's own comment record
        comment = self.document.ca.comment
        # if there is none
        if comment is None:
            # make one that carries the token
            self.document.ca.comment = [None, [token]]
            # all done
            return
        # otherwise, add the token to the pile
        comment[1].append(token)
        # all done
        return

    def _join(self, preamble):
        """
        Fold {preamble}, a list of comment tokens, into one token
        """
        # the first token carries the rest
        token = preamble[0]
        # fold in the others
        token.value = "".join(item.value for item in preamble)
        # and hand it off
        return token


# end of file
