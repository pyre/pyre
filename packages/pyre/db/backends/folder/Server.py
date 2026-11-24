# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import datetime
import decimal
import json
import os
import re
import uuid
import pyre

# superclass
from ... import Server as base

# my exceptions
from ... import exceptions

# the declarations of tables
from ...schema.Table import Table

# the visitor that writes the values of the columns
from .Text import Text


# declaration
class Server(base.Server, family="pyre.db.servers.folder"):
    """
    Component that keeps the tables of a database as files of rows in a folder, one for each table,
    named after it, in the text format of postgres's copies

    A folder holds rows and nothing else: its tables are made and removed, and their rows are
    loaded and read back whole, in the order they were loaded, with the values they brought. The
    requests about indexes and identities leave it as it is, and statements are refused. A
    transaction block that raises leaves the files as it found them
    """

    # the escapes of the text format: a backslash followed by up to three octal digits, by an x
    # and up to two hexadecimal ones, or by any other character
    escape = re.compile(r"\\(x[0-9a-fA-F]{1,2}|[0-7]{1,3}|.)")
    # the characters the letters of the escapes of the control characters stand for
    controls = {"b": "\b", "f": "\f", "n": "\n", "r": "\r", "t": "\t", "v": "\v"}
    # the words postgres reads as truth values
    truths = ("t", "true", "y", "yes", "on", "1")
    # and the ones it reads as falsehoods
    falsehoods = ("f", "false", "n", "no", "off", "0")

    # public state
    path = pyre.properties.path()
    path.default = None
    path.doc = "the folder that holds the files of the tables"

    # interface
    @pyre.export
    def attach(self):
        """
        Make my folder, unless it is there already
        """
        # a server without a folder
        if self.path is None:
            # has nowhere to keep its tables
            raise exceptions.InterfaceError(
                diagnostic=f"the folder server {self.pyre_name} has no folder"
            )
        # make it, along with the folders it is in
        self.path.mkdir(parents=True, exist_ok=True)
        # and hand me back
        return self

    @pyre.export
    def detach(self):
        """
        Let go of my folder, which needs nothing
        """
        # hand me back
        return self

    @pyre.export
    def execute(self, *sql):
        """
        Refuse the statements in {sql}, since a folder only holds rows
        """
        # say so
        raise self._statements()

    def run(self, statement, *arguments):
        """
        Refuse {statement}, since a folder only holds rows
        """
        # say so
        raise self._statements()

    # tables
    def createTable(self, table, existOk=False, indexes=True, selfReferences=True):
        """
        Make the file of the rows of {table}, empty; with {existOk}, finding it there already is
        fine, and its rows are left alone; its rows are read whole and hold the values they were
        given, so {indexes} and {selfReferences} change nothing
        """
        # the file of the table
        file = self._file(table=table)
        # a table that is there already
        if file.exists():
            # is fine when the caller says so
            if existOk:
                # so leave it alone
                return self
            # and a mistake otherwise
            raise exceptions.ProgrammingError(
                diagnostic=f"the table {table.pyre_name} is there already",
                table=table.pyre_name,
            )
        # make it
        file.touch()
        # and hand me back
        return self

    def dropTable(self, table, missingOk=False):
        """
        Remove the file of the rows of {table}; with {missingOk}, finding it gone already is fine
        """
        # a removal inside a transaction block
        if self._snapshots:
            # could not be undone, since the snapshot of the block keeps only the sizes of the files
            raise exceptions.NotSupportedError(
                diagnostic=(
                    f"the table {table.pyre_name} cannot be removed inside a transaction block"
                ),
                table=table.pyre_name,
            )
        # the file of the table
        file = self._file(table=table)
        # a table that is gone already
        if not file.exists():
            # is fine when the caller says so
            if missingOk:
                # so there is nothing to do
                return self
            # and a mistake otherwise
            raise self._missing(table=table)
        # remove it
        os.unlink(file)
        # and hand me back
        return self

    def addSelfReferences(self, table):
        """
        Leave {table} as it is: a folder holds the values its rows were given, which no reference
        checks
        """
        # so leave it alone
        return self

    def createIndexes(self, table, existOk=False):
        """
        Leave {table} as it is: a folder reads its tables whole, which an index cannot speed up
        """
        # so leave it alone
        return self

    def createIndex(self, table, name, existOk=False):
        """
        Leave {table} as it is, as {createIndexes} does
        """
        # so leave it alone
        return self

    def dropIndex(self, table, name, missingOk=False):
        """
        Leave {table} as it is, as {createIndexes} does
        """
        # so leave it alone
        return self

    def restartIdentity(self, table, field, start):
        """
        Leave {table} as it is: the values of {field} are the ones its rows bring
        """
        # so leave it alone
        return self

    # rows
    def insert(self, *records, returning=None, existing=None, key=None, generated=None):
        """
        Append {records} to the files of their tables, as {load} does; a folder hands no rows
        back, and keeps no keys to find the rows that are there already
        """
        # a request for the rows the insert adds
        if returning is not None:
            # cannot be met
            raise exceptions.NotSupportedError(diagnostic="a folder hands back no rows it adds")
        # and neither can one about the rows that are there already
        if existing is not None:
            # since a folder holds its rows without keys to find them by
            raise exceptions.NotSupportedError(
                diagnostic="a folder keeps no keys to find the rows that are there already"
            )
        # load the records
        self.load(*records, generated=generated)
        # and hand nothing back, as an insert does
        return None

    def load(self, *records, generated=None):
        """
        Append {records}, all or nothing, to the files of their tables, every column of each, in
        the order the table declares them; a column left to its default gets the default its
        column declares, and a value for a column whose values the server assigns is refused
        unless {generated} is "keep"
        """
        # in a block of its own, so that the load keeps all of its records or none of them
        with self:
            # go through the groups of records, which refuses the values the server assigns
            for table, _, group in self.sql.loadGroups(*records, generated=generated):
                # the file of the table
                file = self._file(table=table)
                # must be there
                if not file.exists():
                    # or the table is missing
                    raise self._missing(table=table)
                # the lines of the records, written before any of them reaches the file
                lines = [
                    self._text.row(table=table, values=self._values(table=table, record=record))
                    for record in group
                ]
                # append them
                with open(file, "a", encoding="utf-8", newline="") as stream:
                    # one at a time
                    for line in lines:
                        # each on a line of its own
                        print(line, file=stream)
        # all done
        return self

    def select(self, query, limit=None, offset=None):
        """
        Read the rows of {query}, a table, as records; a folder reads whole tables only
        """
        # anything but a whole table
        if not (isinstance(query, type) and issubclass(query, Table)) or (
            limit is not None or offset is not None
        ):
            # is more than a folder can read
            raise exceptions.NotSupportedError(diagnostic="a folder reads whole tables only")
        # the file of the table
        file = self._file(table=query)
        # must be there
        if not file.exists():
            # or the table is missing
            raise self._missing(table=query)
        # read its rows, as records
        yield from self._records(rows=self._rows(table=query, file=file), selection=query)
        # all done
        return

    def interpret(self, column, value, selection):
        """
        Turn {value}, the text of {column} of {selection} in its file, into the type of the
        column
        """
        # attempt to
        try:
            # read it as the column says
            return super().interpret(column=column, value=value, selection=selection)
        # text that is not a value of the type of the column
        except ValueError:
            # is a flaw of the file
            raise exceptions.DataError(
                diagnostic=(
                    f"the file of the table {selection.pyre_name} holds {value!r} in the column"
                    f" {column.name}, which is not a value of its type"
                ),
                table=selection.pyre_name,
                column=column.name,
            ) from None

    # the handlers of the columns, which read the text of their values
    def _pyre_onBoolean(self, schema, value, **kwds):
        """
        Read a truth value
        """
        # the words of the truths
        if value.lower() in self.truths:
            # are true
            return True
        # the words of the falsehoods
        if value.lower() in self.falsehoods:
            # are false
            return False
        # and anything else is not a truth value
        raise ValueError(value)

    def _pyre_onInteger(self, schema, value, **kwds):
        """
        Read an integer
        """
        # from its digits
        return int(value)

    def _pyre_onFloat(self, schema, value, **kwds):
        """
        Read a floating point number
        """
        # from its digits, or the name of a value that is not a number
        return float(value)

    def _pyre_onDecimal(self, schema, value, **kwds):
        """
        Read a fixed point number
        """
        # attempt to
        try:
            # read its digits, or the name of a value that is not a number
            return decimal.Decimal(value)
        # text that is neither
        except decimal.InvalidOperation:
            # is not a fixed point number
            raise ValueError(value) from None

    def _pyre_onBytes(self, schema, value, **kwds):
        """
        Read a string of octets, from its hexadecimal digits
        """
        # octets are written as a backslash, an x and their hexadecimal digits
        if not value.startswith("\\x"):
            # and anything else is not a string of octets
            raise ValueError(value)
        # so read the digits
        return bytes.fromhex(value[2:])

    def _pyre_onDate(self, schema, value, **kwds):
        """
        Read a date
        """
        # in the form of the standard
        return datetime.date.fromisoformat(value)

    def _pyre_onTime(self, schema, value, **kwds):
        """
        Read a time of day
        """
        # in the form of the standard
        return datetime.time.fromisoformat(value)

    def _pyre_onTimestamp(self, schema, value, **kwds):
        """
        Read a moment in time
        """
        # in the form of the standard
        return datetime.datetime.fromisoformat(value)

    def _pyre_onUUID(self, schema, value, **kwds):
        """
        Read a universally unique identifier
        """
        # in its usual form
        return uuid.UUID(value)

    def _pyre_onJSON(self, schema, value, **kwds):
        """
        Read a json document
        """
        # a column read as its text
        if schema._asText:
            # holds the text of its documents
            return value
        # the others hold documents
        return json.loads(value)

    def _pyre_onArray(self, schema, value, **kwds):
        """
        Read an array, as postgres writes its arrays: each level in braces, its entries
        separated by commas, a null as NULL, and an entry in double quotes when it needs them
        """
        # read its levels, down to the texts of its entries
        level, position = self._arrayLevel(text=value, position=0)
        # the array must be the whole text
        if position != len(value):
            # or the text is not an array
            raise ValueError(value)
        # read the entries as the column type of the entries says
        return self._arrayEntries(level=level, schema=schema.schema, **kwds)

    # meta methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # the visitor that writes the values of the columns
        self._text = Text()
        # the sizes of the files of the tables at the start of each open block, innermost last
        self._snapshots = []
        # all done
        return

    # context manager support
    def __enter__(self):
        """
        Open a transaction block, by noting the sizes of the files of the tables
        """
        # note them
        self._snapshots.append(self._sizes())
        # and hand me over
        return self

    def __exit__(self, exc_type, exc_instance, exc_traceback):
        """
        Close a transaction block: one that ends normally keeps its work, and one that raises
        leaves the files as it found them
        """
        # the sizes of the files when the block opened
        sizes = self._snapshots.pop()
        # a block that raised
        if exc_type is not None:
            # undoes its work
            self._restore(sizes=sizes)
        # and re-raise any exception that occurred in the block
        return False

    # implementation details
    def _file(self, table):
        """
        Build the path to the file of the rows of {table}
        """
        # in my folder, named after the table
        return self.path / f"{table.pyre_name}.tsv"

    def _values(self, table, record):
        """
        Build the values of every column of {table} that {record} holds, in order
        """
        # the values
        values = []
        # go through the columns
        for field, value in zip(table.pyre_fields, record):
            # a column left to its default
            if value is table.default:
                # gets the one it declares
                value = field.default
            # a column left to the server
            elif value is None and field._autogenerated:
                # has no value, since the values in a folder are the ones its rows bring
                raise exceptions.NotSupportedError(
                    diagnostic=(
                        f"a folder assigns no values, and the column"
                        f" {table.pyre_name}.{field.name} has none"
                    ),
                    table=table.pyre_name,
                    column=field.name,
                )
            # keep it
            values.append(value)
        # hand them over
        return values

    def _rows(self, table, file):
        """
        Generate the rows of {table} that {file} holds, each one a tuple of the texts of its values,
        with {None} for a null
        """
        # the number of columns of the table
        columns = len(table.pyre_fields)
        # read the file
        with open(file, encoding="utf-8", newline="") as stream:
            # one line at a time
            for number, line in enumerate(stream, start=1):
                # the values of the line, without its end
                fields = line.rstrip("\r\n").split("\t")
                # a line with values for other columns
                if len(fields) != columns:
                    # is a flaw of the file
                    raise exceptions.DataError(
                        diagnostic=(
                            f"line {number} of the file of the table {table.pyre_name} holds"
                            f" {len(fields)} values for its {columns} columns"
                        ),
                        table=table.pyre_name,
                    )
                # the others make a row
                yield tuple(self._unescape(text=field) for field in fields)
        # all done
        return

    def _unescape(self, text):
        """
        Turn {text}, a value as the file holds it, back into the text of the value, or {None} for
        a null
        """
        # a null
        if text == self._text.null:
            # is {None}
            return None
        # the others have their escapes replaced
        return self.escape.sub(self._escaped, text)

    def _escaped(self, match):
        """
        Build the character an escape stands for
        """
        # the part of the escape after the backslash
        code = match.group(1)
        # a hexadecimal escape
        if code[0] == "x" and len(code) > 1:
            # stands for the character with that code
            return chr(int(code[1:], 16))
        # an octal one
        if code[0].isdigit() and code[0] < "8":
            # stands for the character with that code
            return chr(int(code, 8))
        # the others stand for a control character, or for themselves
        return self.controls.get(code, code)

    def _arrayLevel(self, text, position):
        """
        Read the level of an array that starts at {position} of {text}, and hand back its items,
        each a level, the text of an entry, or {None} for a null, and the position after it
        """
        # a level opens with a brace
        if text[position : position + 1] != "{":
            # or it is not a level
            raise ValueError(text)
        # step inside
        position += 1
        # a level that closes right away
        if text[position : position + 1] == "}":
            # is empty
            return (), position + 1
        # the items
        items = []
        # until the level closes
        while True:
            # the character that starts the next item
            start = text[position : position + 1]
            # a level below this one
            if start == "{":
                # is read the same way
                item, position = self._arrayLevel(text=text, position=position)
            # an entry in quotes
            elif start == '"':
                # is read up to its closing quote
                item, position = self._arrayQuoted(text=text, position=position)
            # and any other
            else:
                # is read up to the comma or the brace after it
                item, position = self._arrayBare(text=text, position=position)
            # keep the item
            items.append(item)
            # the character after it
            after = text[position : position + 1]
            # a comma
            if after == ",":
                # leads to another item
                position += 1
                # so read it
                continue
            # a brace
            if after == "}":
                # closes the level
                return tuple(items), position + 1
            # and anything else is not part of an array
            raise ValueError(text)

    def _arrayQuoted(self, text, position):
        """
        Read the entry in double quotes that starts at {position} of {text}, and hand back its
        text and the position after its closing quote
        """
        # the characters of the entry
        characters = []
        # step past the opening quote
        position += 1
        # until the closing quote
        while position < len(text):
            # the next character
            character = text[position]
            # a backslash
            if character == "\\":
                # stands for the character after it
                characters.append(text[position + 1 : position + 2])
                # so step past both
                position += 2
                # and move on
                continue
            # a quote
            if character == '"':
                # closes the entry
                return "".join(characters), position + 1
            # the others stand for themselves
            characters.append(character)
            # so step past it
            position += 1
        # an entry whose quote never closes is not part of an array
        raise ValueError(text)

    def _arrayBare(self, text, position):
        """
        Read the entry without quotes that starts at {position} of {text}, and hand back its text,
        or {None} for a null, and the position of the comma or the brace after it
        """
        # the characters of the entry
        characters = []
        # until a comma or a brace
        while position < len(text) and text[position] not in ",}":
            # a backslash
            if text[position] == "\\":
                # stands for the character after it
                characters.append(text[position + 1 : position + 2])
                # so step past both
                position += 2
                # and move on
                continue
            # the others stand for themselves
            characters.append(text[position])
            # so step past it
            position += 1
        # the text of the entry, without the white space around it
        entry = "".join(characters).strip()
        # an entry without text
        if not entry:
            # is not part of an array
            raise ValueError(text)
        # a null is spelled out
        if entry.upper() == "NULL":
            # and stands for {None}
            return None, position
        # the others stand for their text
        return entry, position

    def _arrayEntries(self, level, schema, **kwds):
        """
        Read the entries of {level}, a level of an array, as {schema}, the column type of its
        entries, says
        """
        # a level
        if isinstance(level, tuple):
            # has its items read the same way
            return tuple(self._arrayEntries(level=item, schema=schema, **kwds) for item in level)
        # a null
        if level is None:
            # stays as it is
            return None
        # and the others are read as their type says
        return schema._pyre_identify(authority=self, value=level, **kwds)

    def _sizes(self):
        """
        Note the sizes of the files of the tables in my folder, by name
        """
        # the files of the tables
        return {
            entry.name: entry.stat().st_size
            for entry in os.scandir(self.path)
            if entry.is_file() and entry.name.endswith(".tsv")
        }

    def _restore(self, sizes):
        """
        Make the files of the tables in my folder what {sizes} says they were: the ones made since
        are removed, and the others cut back to their sizes
        """
        # go through the files there now
        for name in self._sizes():
            # the file
            file = self.path / name
            # one made since
            if name not in sizes:
                # is removed
                os.unlink(file)
                # and that's all for it
                continue
            # the others are cut back to their sizes
            os.truncate(file, sizes[name])
        # all done
        return

    def _missing(self, table):
        """
        Build the exception that reports that {table} is not in my folder
        """
        # say so
        return exceptions.ProgrammingError(
            diagnostic=f"there is no table {table.pyre_name}",
            table=table.pyre_name,
        )

    def _statements(self):
        """
        Build the exception that refuses a statement, since a folder runs none
        """
        # say so
        return exceptions.NotSupportedError(diagnostic="a folder runs no statements")


# end of file
