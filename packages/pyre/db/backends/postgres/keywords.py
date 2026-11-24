# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the words postgres reserves, which a name must be quoted to use: those its {pg_get_keywords}
# puts in the categories R (reserved) and T (reserved, except as a function or a type name),
# as postgres 18 reports them
reserved = frozenset("""
    all analyse analyze and any array as asc asymmetric authorization binary both case cast
    check collate collation column concurrently constraint create cross current_catalog
    current_date current_role current_schema current_time current_timestamp current_user default
    deferrable desc distinct do else end except false fetch for foreign freeze from full grant
    group having ilike in initially inner intersect into is isnull join lateral leading left
    like limit localtime localtimestamp natural not notnull null offset on only or order outer
    overlaps placing primary references returning right select session_user similar some
    symmetric system_user table tablesample then to trailing true union unique user using
    variadic verbose when where window with
    """.split())


# end of file
