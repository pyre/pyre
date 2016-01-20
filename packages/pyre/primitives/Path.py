# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# externals
import collections, functools, io, os, pwd, stat


# helpers
def _unary(f):
    """
    Wrapper for functions that require the string representation of path objects
    """
    # wrap
    @functools.wraps(f)
    def dispatch(self, *args, **kwds):
        # build my rep and forward to the wrapped function
        return f(str(self), *args, **kwds)
    # build the method
    return dispatch


# declaration
class Path(tuple):
    """
    A representation of a path
    """

    # string constants
    _CWD = '.'
    _SEP = '/'

    # path constants
    root = None


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
    def names(self):
        """
        Build an iterator over the names of my components, skipping the root marker, if present
        """
        # grab my parts
        parts = self.parts
        # if I am an absolute path
        if self.anchor:
            # advance the counter
            next(parts)
        # and return the iterator
        return parts


    @property
    def anchor(self):
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
        Build a path that is my logical ancestor

        Note that this is purely a lexical operation and is not guaranteed to yield correct
        results unless this path has been fully resolved
        """
        # the root
        if self == self.root:
            # is it's own parent
            return self
        # for the rest, generate a sequence of length one shorter than me
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


    @property
    def contents(self):
        """
        Generate a sequence of my contents
        """
        # go through my contents
        for name in os.listdir(str(self)):
            # make a path and hand it to the caller
            yield self / name
        # all done
        return


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
        if self.anchor:
            # splice my representation into a valid 'file:' uri
            return "file://{}".format(self)
        # otherwise, build an error message
        msg = "'{}' is a relative path and can't be expressed as a URI".format(self)
        # and complain
        raise ValueError(msg)


    def isAbsolute(self):
        """
        Check whether the path is absolute or not
        """
        # get my last part
        return True if self.anchor else False


    def isReserved(self):
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


    def relativeTo(self, other):
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


    def withName(self, name):
        """
        Build a new path with my name replaced by {name}
        """
        # check that the name has no separators in it
        if self._SEP in name:
            # complain
            raise ValueError("invalid name {!r}".format(str(name)))
        # replace my name and build a new path
        return super().__new__(type(self), (name,) + self[1:])


    def withSuffix(self, suffix=None):
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
                return self.withName(stem)
            # otherwise,  clone me
            return self

        # if a suffix were supplied, append it to my stem and build a path
        return self.withName(name=stem+suffix)


    # real path interface
    @classmethod
    def cwd(cls):
        """
        Build a path that points to the current working directory
        """
        # get the directory and turn it into a path
        return cls(os.getcwd())


    @classmethod
    def home(cls, user=''):
        """
        Build a path that points to the {user}'s home directory
        """
        # grab the {pwd} support
        import pwd
        # if we don't have a user
        if not user:
            # assume the current user
            dir = pwd.getpwuid(os.getuid()).pw_dir
        # otherwise
        else:
            # attempt to
            try:
                # index the {passwd} database using the user
                dir = pwd.getpwnam(user).pw_dir
            # if this fails
            except KeyError:
                # most likely cause is
                msg = "the user {!r} is not in the password database".format(user)
                # so complain
                raise RuntimeError(msg)
        # if we get this far, we have the name of the path; build a path and return it
        return cls(dir)


    def resolve(self):
        """
        Build an equivalent absolute normalized path that is free of symbolic links
        """
        # if I'm empty
        if not self:
            # return the current working directory
            return self.cwd()
        # if I am the root
        if self == self.root:
            # I am already resolved
            return self
        # otherwise, get the guy to do his thing
        resolution = self._resolve(resolved={})
        # check that it exists
        resolution.stat()
        # and return it
        return resolution


    def expanduser(self):
        """
        Build a path with '~' and '~user' patterns expanded
        """
        # grab the user spec, which must be my leading path component
        spec = self[-1]
        # if it doesn't start with the magic character
        if spec[0] != '~':
            # we are done
            return self
        # otherwise, use it to look up the user's home directory; the user name is what follows
        # the marker, and our implementation of {home} interprets a blank user name as the
        # current user
        home = self.home(user=spec[1:])
        # build the new path and return it
        return super().__new__(type(self), self[:-1] + home)


    # real path introspection
    def exists(self):
        """
        Check whether I exist
        """
        # attempt to
        try:
            # get my stat record
            self.stat()
        # if i don't exist or i am a broken link
        except (FileNotFoundError, NotADirectoryError):
            # stat is unhappy, so i don't exist
            return None
        # if i got this far, i exist
        return True


    def isBlockDevice(self):
        """
        Check whether I am a block device
        """
        # check with {stat}
        return self.amI(stat.S_ISBLK)


    def isCharacterDevice(self):
        """
        Check whether I am a character device
        """
        # check with {stat}
        return self.amI(stat.S_ISCHR)


    def isDirectory(self):
        """
        Check whether I am a directory
        """
        # check with {stat}
        return self.amI(stat.S_ISDIR)


    def isFile(self):
        """
        Check whether I am a regular file
        """
        # check with {stat}
        return self.amI(stat.S_ISREG)


    def isNamedPipe(self):
        """
        Check whether I am a socket
        """
        # check with {stat}
        return self.amI(stat.S_ISFIFO)


    def isSocket(self):
        """
        Check whether I am a socket
        """
        # check with {stat}
        return self.amI(stat.S_ISSOCK)


    def isSymlink(self):
        """
        Check whether I am a symbolic link
        """
        # attempt to
        try:
            # get my stat record
            mode = self.lstat().st_mode
        # if anything goes wrong:
        except (AttributeError, FileNotFoundError, NotADirectoryError):
            # links are probably not supported here, so maybe not...
            return False
        # otherwise, check with my stat record
        return stat.S_ISLNK(mode)


    def amI(self, mask):
        """
        Get my stat record and filter me through {mask}
        """
        # attempt to
        try:
            # get my stat record
            mode = self.stat().st_mode
        # if i don't exist or i am a broken link
        except (FileNotFoundError, NotADirectoryError):
            # probably not...
            return False
        # otherwise, check with {mask}
        return mask(mode)


    # forwarding to standard library functions
    stat = _unary(os.stat)
    lstat = _unary(os.lstat)
    mkdir = _unary(os.mkdir)
    open = _unary(io.open)


    # meta-methods
    def __new__(cls, *args):
        """
        Build a new path out of strings or other paths
        """
        # if i have only one argument and it is a path
        if len(args) == 1 and isinstance(args[0], cls):
            # return it
            return args[0]
        # otherwise, parse the arguments and chain up to build my instance
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


    # arithmetic; pure sugar but slower than other methods of assembling paths
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
                # path fragments that are absolute paths are supposed to reset the path; since
                # we traverse the sequence in reverse order, this means we have to go no
                # further
                if arg and arg[0] == sep:
                    # mark as an absolute path
                    yield sep
                    # and terminate the sequence
                    return
            # more general iterables
            elif isinstance(arg, collections.abc.Iterable):
                # recurse with their contents
                yield from cls._parse(args=arg, sep=sep)
            # anything else
            else:
                # is an error
                msg = "can't parse '{}', of type {}".format(arg, type(arg))
                # so complain
                raise TypeError(msg)

        # all done
        return


    def _resolve(self, base=None, resolved=None):
        """
        Workhorse for path resolution
        """
        # what's left to resolve
        workload = self.parts
        # if i am an absolute path
        if self.anchor:
            # set my starting point
            base = self.root
            # skip the leasing root marker
            next(workload)
        # if i am a relative path
        else:
            # my starting point is the current working directory, which is guaranteed to be
            # free of symbolic links
            base = self.cwd() if base is None else base

        # at this point, {base} is known to be a fully resolved path
        # go through my parts
        for part in workload:
            # empty or parts that are '.'
            if not part or part=='.':
                # are skipped
                continue
            # parent directory markers
            if part == '..':
                # back me up by one level
                base = base.parent
                # and carry on
                continue
            # splice the part onto base
            newpath = base / part
            # check
            try:
                # whether we have been here before
                resolution = resolved[newpath]
            # if not
            except KeyError:
                # carry on
                pass
            # if yes
            else:
                # if {base} has a null resolution
                if resolution is None:
                    # we got a loop
                    msg = "while resolving '{}': symbolic link loop at '{}'".format(self, newpath)
                    # so complain
                    raise RuntimeError(msg)
                # otherwise, replace {base} with its resolution
                base = resolution
                # and carry on
                continue

            # now we need to know whether what we have so far is a symbolic link
            if newpath.isSymlink():
                # add it to the pile, but mark it unresolved
                resolved[newpath] = None
                # find out what it points to
                link = type(self)(os.readlink(str(newpath)))
                # resolve it in my context
                base = link._resolve(resolved=resolved, base=base)
                # remember this
                resolved[newpath] = base
            # if not
            else:
                # save it and carry on
                base = newpath

        return base


# patches
Path.root = Path(Path._SEP)


# end of file
