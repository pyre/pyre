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
            token = self._take(node=container[key], fallback=(container, key))
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
        # find the entry that precedes the one being removed, if any
        siblings = (
            list(container.keys())
            if isinstance(container, self.Map)
            else list(range(len(container)))
        )
        index = siblings.index(key)
        previous = siblings[index - 1] if index > 0 else None
        # the comment block that trails the entry must survive its removal
        token = self._take(node=container[key], fallback=(container, key))
        # except for a comment on the line of the entry itself, which describes what is going
        token = self._detach(token=token)
        # the lines that precede the entry as well
        preamble = self._takePreamble(container=container, key=key)
        # remove the entry
        del container[key]
        # the container's own place in its parent, for when the removal empties it
        parent = (self.get(*path[:-2]), path[-2]) if len(path) > 1 else None
        # settle the comments where the entry was: after the entry that preceded it, or at the
        # head of the container when it was first
        self._settle(
            container=container,
            previous=previous,
            preamble=preamble,
            token=token,
            parent=parent,
        )
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

    def find(self, name):
        """
        Find the key path of the entry that configures {name}, a dotted pyre name, resolving
        the scoping of configuration files: a key may spell several levels of the name, and
        may carry a family before a '#'
        """
        # the levels of the name
        levels = name.split(".")
        # start at the top
        return self._find(node=self.document, levels=levels, path=())

    def locate(self, line):
        """
        Find the key path of the entry whose key sits on {line}, counting from one
        """
        # the backend counts from zero
        return self._locate(node=self.document, line=line - 1, path=())

    def render(self):
        """
        Build the text of the document
        """
        # comments held for containers that never got an entry cannot go on the key of the
        # empty container, since the backend renders them between the key and the brackets;
        # they were headed for the tail of the document, so they go after the last entry
        # that can carry them
        for fallback, token in self._held.values():
            # an empty collection that is the last entry of the document is the one place
            # the backend renders a comment on its key correctly, after the brackets
            if fallback == self._tail(node=self.document):
                # so the comment goes on the key
                container, key = fallback
                self._slot(container=container, key=key)[self._position(container=container)] = (
                    token
                )
                # and on to the next one
                continue
            # otherwise, the comment settles near the container, after the entry that
            # precedes it, as if it trailed an entry removed from that spot
            container, key = fallback
            siblings = (
                list(container.keys())
                if isinstance(container, self.Map)
                else list(range(len(container)))
            )
            index = siblings.index(key)
            self._settle(
                container=container,
                previous=siblings[index - 1] if index > 0 else None,
                preamble=None,
                token=token,
                parent=None,
            )
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
    def _find(self, node, levels, path):
        """
        Look for the entry that spells {levels} within {node}, a mapping at {path}
        """
        # anything but a mapping holds no entries
        if not isinstance(node, self.Map):
            # so the search fails
            return None
        # go through the keys
        for key in node:
            # the name of the entry is the key, or what follows the family in it
            spelled = str(key).split("#", 1)[-1].strip().split(".")
            # if it spells more of the name than there is
            if len(spelled) > len(levels):
                # it is not the one
                continue
            # if it does not spell the head of the name
            if levels[: len(spelled)] != spelled:
                # move on
                continue
            # if it spells the whole name
            if len(spelled) == len(levels):
                # this is the entry
                return path + (key,)
            # otherwise, the rest of the name is spelled below it
            found = self._find(node=node[key], levels=levels[len(spelled) :], path=path + (key,))
            # if it was found there
            if found is not None:
                # hand it off
                return found
        # not here
        return None

    def _locate(self, node, line, path):
        """
        Look for the entry whose key sits on {line}, counting from zero, within {node}
        """
        # anything but a mapping has no keys
        if not isinstance(node, self.Map):
            # so the search fails
            return None
        # go through the keys
        for key in node:
            # carefully, since keys the editor added have no line
            try:
                # get the position of the key
                position = node.lc.key(key)
            # if the backend has no record of it
            except KeyError:
                # it is not on any line
                position = None
            # a key without a position is not on any line either
            where = position[0] if position else None
            # if it is the one
            if where == line:
                # this is the entry
                return path + (key,)
            # otherwise, look below it
            found = self._locate(node=node[key], line=line, path=path + (key,))
            # if it was found there
            if found is not None:
                # hand it off
                return found
        # not here
        return None

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
            # if the key is missing, or holds a bare key left behind by an emptied section
            if not self._holds(node=node, key=key) or node[key] is None:
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

    def _anchor(self, node):
        """
        Find the container and key of the last entry of {node} that can carry a trailing
        comment: the deepest last entry whose value is not an empty collection, looking back
        through earlier entries when the last ones are empty
        """
        # anything but a container has no entries
        if not isinstance(node, (self.Map, self.Seq)):
            # so there is nothing here
            return None
        # the entries
        keys = list(node.keys()) if isinstance(node, self.Map) else list(range(len(node)))
        # go through them, last first
        for key in reversed(keys):
            # get the value
            value = node[key]
            # a scalar can carry the comment
            if not isinstance(value, (self.Map, self.Seq)):
                # so this is the anchor
                return node, key
            # a collection carries it on its own anchor
            anchor = self._anchor(node=value)
            # if it has one
            if anchor is not None:
                # that is it
                return anchor
        # nothing here can carry it
        return None

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

    def _take(self, node, residue=False, fallback=None):
        """
        Detach and return the comment block that trails the deepest last entry of {node}, or
        the one at {fallback}, a container and key, when {node} has no entries

        With {residue} set, the blank lines that open the block stay behind, to set the old
        tail apart from the new top level section about to follow it
        """
        # find the tail
        container, key = self._tail(node=node)
        # a node without entries carries its block at the fallback
        if container is None:
            # if there is none
            if fallback is None:
                # there is nothing to take
                return None
            # otherwise, unpack it
            container, key = fallback
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

    def _detach(self, token):
        """
        Strip {token} of the comment on the line of its entry, keeping the block below it
        """
        # nothing to strip
        if token is None:
            # is nothing to do
            return None
        # get the text
        text = token.value
        # a block starts on the line after the entry
        cut = text.find("\n")
        # if the token holds nothing but an inline comment
        if cut < 0 or not text[cut:].strip():
            # there is no block
            return None
        # otherwise, keep the block
        token.value = text[cut:]
        # and hand it off
        return token

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

    def _settle(self, container, previous, preamble, token, parent):
        """
        Place the comments of an entry removed from {container} where the entry was: after
        {previous}, the entry that preceded it, or at the head of the container when there is
        none; a container left empty hands them to its own entry in {parent}. Comments that
        described the removed entry survive, since the editor cannot tell them apart from
        comments about its neighbors
        """
        # the lines that preceded the entry come first, then the block that trailed it
        tokens = [item for item in (self._join(preamble), token) if item is not None]
        # if there is nothing to place
        if not tokens:
            # there is nothing to do
            return
        # if the removal emptied the container and it has a place in its parent, the comments
        # cannot stay inside it: the backend has no place for a comment after an empty
        # collection, and a comment on its key renders between the key and the brackets
        if not len(container) and parent is not None:
            # unpack the place
            grandparent, key = parent
            # an emptied mapping becomes a bare key, which means the same to the configuration
            # loader and carries the comments after its line
            if isinstance(container, self.Map):
                # replace it
                grandparent[key] = None
                # and place the comments after the key
                for item in tokens:
                    # one by one
                    self._append(container=grandparent, key=key, token=item)
                # all done
                return
            # an emptied list keeps its brackets, since a bare key would not mean an empty
            # list; the comments move above it, after the entry that precedes it
            siblings = (
                list(grandparent.keys())
                if isinstance(grandparent, self.Map)
                else list(range(len(grandparent)))
            )
            index = siblings.index(key)
            before = siblings[index - 1] if index > 0 else None
            # and settle there, as if the list itself had been removed
            self._settle(
                container=grandparent,
                previous=before,
                preamble=tokens,
                token=None,
                parent=None,
            )
            # all done
            return
        # if there is no entry ahead of the removed one
        if previous is None:
            # the comments lead the container
            for item in tokens:
                # one by one
                self._lead(container=container, token=item)
            # all done
            return
        # otherwise, they trail the last entry of the previous one that can carry them, or
        # the previous entry itself when it is a scalar
        tail, key = self._anchor(node=container[previous]) or (container, previous)
        # place them
        for item in tokens:
            # after whatever already trails the entry
            self._append(container=tail, key=key, token=item)
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
        # otherwise, join the texts; the token opens with the newline that ended the line of
        # its old entry, and the block it joins already ends its line, so that newline goes
        text = token.value[1:] if token.value.startswith("\n") else token.value
        slot[position].value = slot[position].value + text
        # all done
        return

    def _lead(self, container, token):
        """
        Add {token} to the comments that lead {container}, ahead of its first entry
        """
        # the token opens with the newline that ended the line of its old entry; a leading
        # comment starts a line of its own, so that newline goes
        token.value = token.value[1:] if token.value.startswith("\n") else token.value
        # the container's own comment record
        comment = container.ca.comment
        # if there is none
        if comment is None:
            # make one that carries the token
            container.ca.comment = [None, [token]]
            # all done
            return
        # if the record has no pile of leading comments
        if comment[1] is None:
            # start one
            comment[1] = []
        # add the token to the pile
        comment[1].append(token)
        # all done
        return

    def _join(self, preamble):
        """
        Fold {preamble}, a list of comment tokens, into one token
        """
        # nothing folds into nothing
        if not preamble:
            # so say so
            return None
        # the first token carries the rest
        token = preamble[0]
        # fold in the others
        token.value = "".join(item.value for item in preamble)
        # a preamble is a block of lines that ends with its own newline; the token that trails
        # an entry opens with the newline that ends the entry's line, so give it one
        token.value = token.value if token.value.startswith("\n") else "\n" + token.value
        # and hand it off
        return token


# end of file
