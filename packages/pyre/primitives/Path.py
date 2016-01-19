# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# externals
import collections


# declaration
class Path(tuple):
    """
    A representation of a path
    """


    # constants
    _CWD = '.'
    _SEP = '/'


    # interface
    # methods about me and my parts implemented as properties
    @property
    def parts(self):
        """
        Build an iterator over my components
        """
        # easy enough
        return reversed(self)


    @property
    def root(self):
        """
        Return the representation of the root of the path, if present
        """
        # if i am empty
        if not self:
            # i can't be absolute
            return ''
        # get my last part
        last = self[-1]
        # if it is my separator
        if last == self._SEP:
            # i have a root
            return last
        # otherwise, I don't
        return ''


    @property
    def anchor(self):
        """
        Return the representation of the root of the path, if present
        """
        # don't reimplement
        return self.root


    @property
    def parents(self):
        """
        Generate a sequence of the logical ancestors of the path
        """
        # get my type
        cls = type(self)
        # generate a sequence of lengths so i can build subsequences
        for pos in range(1,len(self)):
            # build a path out of a subsequence that doesn't include the first level; get {new}
            # from my superclass to do this so we can avoid the double reverse
            yield super().__new__(type(self), self[pos:])
        # all done
        return


    @property
    def parent(self):
        """
        Generate a sequence of the logical ancestors of the path
        """
        # generate a sequence of length one shorter than me and turn it into a path
        return super().__new__(type(self), self[1:])


    @property
    def name(self):
        """
        Return the final path component
        """
        # when i am empty
        if not self:
            # the last component is the empty string
            return ''
        # otherwise, get my first entry, which is the last part of the path
        name = self[0]
        # return it, unless it's the separator, in which case return the empty string
        return name if name != self._SEP else ''


    @property
    def path(self):
        """
        Return a string representing the full path
        """
        # easy enough
        return str(self)


    @property
    def suffix(self):
        """
        The file extension of the final path component
        """
        # grab my name
        name = self.name
        # look for the last '.'
        pos = name.rfind('.')
        # if not there
        if pos == -1:
            # we have nothing
            return ''
        # otherwise
        return name[pos:]


    @property
    def suffixes(self):
        """
        Return an iterable over the extensions in name
        """
        # get my name and skip any leading dots
        name = self.name.lstrip('.')
        # split on the '.', skip the first bit and return the rest with a leading '.'
        return ('.' + suffix for suffix in name.split('.')[1:])


    @property
    def stem(self):
        """
        The final path component without the last suffix
        """
        # grab my name
        name = self.name
        # look for the last '.'
        pos = name.rfind('.')
        # if not there
        if pos == -1:
            # we have nothing
            return ''
        # otherwise
        return name[:pos]


    # introspection methods
    def as_posix(self):
        """
        Return a POSIX compliant representation
        """
        # i know how to do this
        return str(self)


    def as_uri(self):
        """
        Return a POSIX compliant representation
        """
        # if i am an absolute path
        if self.root:
            # splice my representation into a valid 'file:' uri
            return "file://{}".format(self)
        # otherwise, build an error message
        msg = "'{}' is a relative path and can't be expressed as a URI".format(self)
        # and complain
        raise ValueError(msg)


    def is_absolute(self):
        """
        Check whether the path is absolute or not
        """
        # get my last part
        return True if self.root else False


    def is_reserved(self):
        """
        Check whether the path is reserved or not
        """
        # always false
        return False


    # methods about me and others
    def join(self, *others):
        """
        Combine me with {others} and make a new path
        """
        # get my type
        cls = type(self)
        # that's just what my constructor does
        return cls.__new__(cls, self, *others)


    def relative_to(self, other):
        """
        Find a {path} such that {other} / {path} == {self}
        """
        # the {path} exists iff {other} is a subsequence of {self}
        for mine, hers in zip(reversed(self), reversed(other)):
            # if they are not identical
            if mine != hers:
                # build the message
                msg = "{!r} does not start with {!r}".format(str(self), str(other))
                # and complain
                raise ValueError(msg)

        # what's left is the answer
        return super().__new__(type(self), self[:len(other)+1])


    def with_name(self, name):
        """
        Build a new path with my name replaced by {name}
        """
        # check that the name has no separators in it
        if self._SEP in name:
            # complain
            raise ValueError("invalid name {!r}".format(str(name)))
        # drop my name and build a new one path to spec
        return super().__new__(type(self), (name,) + self[1:])


    def with_suffix(self, suffix=None):
        """
        Build a new path with my suffix replaced by {suffix}
        """
        # check that the suffix is valid
        if suffix and (not suffix.startswith('.') or self._SEP in suffix):
            # complain
            raise ValueError("invalid suffix {!r}".format(str(suffix)))
        # get my name
        name = self.name
        # get my suffix
        mine = self.suffix
        # and my stem
        stem = self.stem

        # if the suffix is {None}
        if suffix is None:
            # and i have one
            if mine:
                # remove it
                return self.with_name(stem)
            # otherwise,  clone me
            return super().__new__(type(self), self)

        # otherwise, build a path with my stem and the given suffix
        return self.with_name(name=stem+suffix)

    # meta-methods
    def __new__(cls, *args):
        """
        Build a new path out of strings or other paths
        """
        # chain up to build my instance
        return super().__new__(cls, cls._parse(args))


    def __str__(self):
        """
        Assemble my parts into a string
        """
        # if i am empty
        if not self:
            # i represent the current working directory
            return self._CWD
        # grab my separator
        sep = self._SEP
        # prime a reverse iterator over my parts
        rev = reversed(self)
        # if i am an absolute path
        if self[-1] == sep:
            # advance the iterator to skip the root marker
            next(rev)
            # but remember it
            marker = sep
        # otherwise
        else:
            # leave no marker in the beginning
            marker = ''
        # ok, let's put this all together
        return '{}{}'.format(marker, sep.join(rev))


    def __truediv__(self, other):
        """
        Syntactic sugar for assembling paths
        """
        # get my type
        cls = type(self)
        # too easy
        return cls.__new__(cls, self, other)


    def __rtruediv__(self, other):
        """
        Syntactic sugar for assembling paths
        """
        # get my type
        cls = type(self)
        # too easy
        return cls.__new__(cls, other, self)


    # implementation details
    @classmethod
    def _parse(cls, args, sep=_SEP):
        """
        Recognize each entry in {args} and distill its contribution to the path under construction
        """
        # go through the {args}
        for arg in reversed(args):
            # if {arg} is another path
            if isinstance(arg, cls):
                # append its part to mine
                yield from arg
                # if this is an absolute path
                if arg[-1] == sep:
                    # and terminate the sequence
                    return
            # if {arg} is a string
            elif isinstance(arg, str):
                # split on separator, reverse the sequence of parts, and then remove blanks
                # caused by multiple consecutive separators
                yield from filter(None, reversed(arg.split(sep)))
                # check whether this string started with a slash
                if arg[0] == sep:
                    # send the marker
                    yield sep
                    # and terminate the sequence
                    return
            # more general iterables
            elif isinstance(arg, collections.abc.Iterable):
                # recurse
                yield from cls._parse(args=arg, sep=sep)
            # anything else
            else:
                # is an error
                msg = "can't parse '{}', of type {}".format(arg, type(arg))
                # so complain
                raise TypeError(msg)

        # all done
        return


# end of file
