# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


class Path(tuple):
    """
    A representation of a path
    """


    # constants
    sep = '/'


    # interface
    @property
    def parts(self):
        """
        Build an iterator over my components
        """
        # easy enough
        return reversed(self)


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
        return name if name != self.sep else ''


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
        # grab my separator
        sep = self.sep
        # prime a reverse iterator over my parts
        rev = reversed(self)
        # if i am a rooted path
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
    def _parse(cls, args, sep=sep):
        """
        Recognize each entry in {args} and distill its contribution to the path under construction
        """
        # go through the {args}
        for arg in reversed(args):
            # if {arg} is another path
            if isinstance(arg, cls):
                # append its part to mine
                yield from arg
                # if this is a rooted path
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
        # all done
        return


# end of file
