# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
This file collects the table declarations for the {bizbook} database from 

    "The Practical SQL Handbook", Second Edition
    Judith S. Bowman
    Sandra L. Emerson
    Marcy Darnovsky
"""


# access the package
import pyre.db


class Location(pyre.db.table, id="locations"):
    """
    The table of locations
    """
    id = pyre.db.str().primary()
    address = pyre.db.str()
    city = pyre.db.str()
    state = pyre.db.str()
    zip = pyre.db.str()


class Person(pyre.db.table, id="persons"):
    """
    The table of people
    """
    ssn = pyre.db.str().primary()
    lastname = pyre.db.str()
    firstname = pyre.db.str()


class Publisher(pyre.db.table, id="publishers"):
    """
    The book publishers
    """
    id = pyre.db.str().primary()
    name = pyre.db.str()
    headquarters = pyre.db.reference(key=Location.id)


class Address(pyre.db.table, id="addresses"):
    """
    The table of addresses
    """
    person = pyre.db.reference(key=Person.ssn)
    address = pyre.db.reference(key=Location.id)

class Staff(pyre.db.table, id="staff"):
    """
    Information about employee roles
    """
    person = pyre.db.reference(key=Person.ssn)
    position = pyre.db.str()

class ContactMethod(pyre.db.table, id="contact_methods"):
    """
    Contact information
    """
    uid = pyre.db.str()
    method = pyre.db.str()
    person = pyre.db.reference(key=Person.ssn)

class Book(pyre.db.table, id="books"):
    """
    Books
    """
    id = pyre.db.str().primary()
    title = pyre.db.str()
    category = pyre.db.str()
    publisher = pyre.db.reference(key=Publisher.id)
    date = pyre.db.str()
    price = pyre.db.decimal(precision=11, scale=2)
    advance = pyre.db.decimal(precision=8, scale=2)
    description = pyre.db.str()

class Author(pyre.db.table, id="authors"):
    """
    Author information
    """
    author = pyre.db.reference(key=Person.ssn)
    book = pyre.db.reference(key=Book.id)
    ordinal = pyre.db.int()
    share = pyre.db.decimal(precision=4, scale=3)

class Editor(pyre.db.table, id="editors"):
    """
    Editor information
    """
    editor = pyre.db.reference(key=Person.ssn)
    book = pyre.db.reference(key=Book.id)
    ordinal = pyre.db.int()

class Invoice(pyre.db.table, id="invoices"):
    """
    Invoices
    """
    id = pyre.db.str().primary()
    client = pyre.db.str()
    po = pyre.db.str()
    date = pyre.db.str()

class InvoiceItem(pyre.db.table, id="invoice_item"):
    """
    Invoice line items
    """
    invoice = pyre.db.reference(key=Invoice.id)
    book = pyre.db.reference(key=Book.id)
    ordered = pyre.db.int()
    shipped = pyre.db.int()
    date = pyre.db.str()


# end of file 
