# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import collections.abc  # for container identification

# to get the base exception
import pyre

# superclass
from .Container import Container


# declaration
class Mapping(Container):
    """
    The base class for type declarators that map strings to other types
    """

    # constants
    typename = "mapping"  # the name of my type
    container = dict  # the default container i represent
    complaint = "could not coerce {0.value!r} to a mapping"
    delimiter = ","  # the separator of the entries in the text form
    separator = ":"  # the separator of a key from its value in the text form

    # interface
    def string(self, value):
        """
        Render {value} as text that can be persisted for later coercion
        """
        # respect {None}
        if value is None:
            # by leaving it alone
            return None
        # get my schema
        schema = self.schema
        # render each entry as its key and the text of its value, and put them together
        return f"{self.delimiter} ".join(
            f"{key}{self.separator}{schema.string(item)}" for key, item in value.items()
        )

    def json(self, value):
        """
        Generate a JSON representation of {value}
        """
        # respect {None}
        if value is None:
            # by leaving it alone
            return None
        # get my schema
        schema = self.schema
        # ask it for the representation of each value
        return {key: schema.json(item) for key, item in value.items()}

    def render(self, renderer, value, incognito=False, **kwds):
        """
        Render {value} using {renderer}
        """
        # a mapping fits on one line, in the form its text is read back from
        entry = self.string(value)
        # if i'm incognito
        if incognito:
            # render just my value
            yield renderer.value(value=entry)
        # otherwise
        else:
            # render both my name and the value
            yield renderer.trait(name=self.name, value=entry)
        # all done
        return

    # visiting
    def _pyre_identify(self, authority, **kwds):
        """
        Let {authority} know i am a mapping
        """
        # attempt to
        try:
            # ask {authority} for my handler
            handler = authority._pyre_onMapping
        # if it doesn't understand
        except AttributeError:
            # chain up
            return super()._pyre_identify(authority=authority, **kwds)
        # otherwise, invoke the handler
        return handler(schema=self, **kwds)

    # implementation details
    def _coerce(self, value, **kwds):
        """
        Convert {value} into a container
        """
        # go through the entries
        for key, entry in self._entries(value=value):
            # attempt to
            try:
                # convert each value and hand it to the caller. perform the conversion
                # incognito, in case coercing my values requires the instantiation of
                # components; i don't want facilities to use the name of my node as the name of
                # any instantiated components
                yield key, self.schema.coerce(value=entry, incognito=True, **kwds)
            # if anything goes wrong that it is managed by the framework
            except pyre.PyreError as error:
                # leave the entry out, and say why
                self._skip(entry=f"{key}{self.separator}{entry}", reason=str(error))
        # all done
        return

    def _entries(self, value):
        """
        Generate the (key, value) pairs in {value}, a mapping, an iterable of pairs, or text of
        the form "key:value, key:value", leaving the values as they are; keys are strings, as
        they are in configuration files, and entries that are not pairs are left out
        """
        # if we have text
        if isinstance(value, str):
            # go through its entries
            for entry in value.split(self.delimiter):
                # clean it up
                entry = entry.strip()
                # skip blank entries, such as the one after a trailing delimiter
                if not entry:
                    # on to the next
                    continue
                # split the key from its value at the first separator, so values may hold more
                key, separator, item = entry.partition(self.separator)
                # an entry without a key
                if not separator or not key.strip():
                    # is left out
                    self._skip(
                        entry=entry, reason=f"it is not of the form 'key{self.separator}value'"
                    )
                    # on to the next
                    continue
                # hand off the pair
                yield key.strip(), item.strip()
            # all done
            return

        # if we have a mapping
        if isinstance(value, collections.abc.Mapping):
            # go through its entries
            for key, entry in value.items():
                # and hand each one off, with its key as a string
                yield str(key), entry
            # all done
            return

        # if we have an iterable
        if isinstance(value, collections.abc.Iterable):
            # go through each entry
            for entry in value:
                # anything that is not a pair, such as a string, which would unpack as one
                if (
                    isinstance(entry, (str, bytes))
                    or not isinstance(entry, collections.abc.Sized)
                    or len(entry) != 2
                ):
                    # is left out
                    self._skip(entry=entry, reason="it is not a (key, value) pair")
                    # on to the next
                    continue
                # unpack the pair
                key, item = entry
                # and hand it off, with its key as a string
                yield str(key), item
            # all done
            return

        # otherwise, flag it as bad input
        raise self.CastingError(value=value, description=self.complaint)

    def _skip(self, entry, reason: str) -> None:
        """
        Report that {entry} is left out of the mapping, because of {reason}
        """
        # get the journal; not when this module is loaded, since that happens while pyre boots,
        # before the journal can find its devices
        import journal

        # make a channel
        channel = journal.warning("pyre.config.containers")
        # say which entry is left out, and why
        channel.log(f"skipping {entry!r}: {reason}")
        # all done
        return


# end of file
