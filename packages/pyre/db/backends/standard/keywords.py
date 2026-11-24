# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the words SQL:2016 reserves, which a name must be quoted to use, as the table of key words in
# the appendix of the postgres 18 documentation lists them. the web page of that table puts a
# zero-width space after each underscore of a long word, so a browser may break it across lines;
# the space is invisible, and a copy of the page carries it along, which is how three of the words
# below, array_max_cardinality, current_default_transform_group and
# current_transform_group_for_type, came to hold them. a word that holds one matches no name, so
# a name spelled like it would go out unquoted; the words are spelled here in printable ASCII,
# which {tests/pyre.pkg/db/identifier_reserved_spelling.py} checks
reserved = frozenset("""
    abs absent acos all allocate alter and any are array array_agg array_max_cardinality as
    asensitive asin asymmetric at atan atomic authorization avg begin begin_frame
    begin_partition between bigint binary blob boolean both by call called cardinality cascaded
    case cast ceil ceiling char char_length character character_length check classifier clob
    close coalesce collate collect column commit condition connect constraint contains convert
    copy corr corresponding cos cosh count covar_pop covar_samp create cross cube cume_dist
    current current_catalog current_date current_path current_role current_row current_schema
    current_time current_timestamp current_user current_default_transform_group
    current_transform_group_for_type cursor cycle datalink date day deallocate dec decfloat
    decimal declare default define delete dense_rank deref describe deterministic disconnect
    distinct dlnewcopy dlpreviouscopy dlurlcomplete dlurlcompleteonly dlurlcompletewrite
    dlurlpath dlurlpathonly dlurlpathwrite dlurlscheme dlurlserver dlvalue double drop dynamic
    each element else empty end end-exec end_frame end_partition equals escape every except exec
    execute exists exp external extract false fetch filter first_value float floor for foreign
    frame_row free from full function fusion get global grant group grouping groups having hold
    hour identity import in indicator initial inner inout insensitive insert int integer
    intersect intersection interval into is join json_array json_arrayagg json_exists
    json_object json_objectagg json_query json_table json_table_primitive json_value lag
    language large last_value lateral lead leading left like like_regex listagg ln local
    localtime localtimestamp log log10 lower match match_number match_recognize matches max
    member merge method min minute mod modifies module month multiset national natural nchar
    nclob new no none normalize not nth_value ntile null nullif numeric occurrences_regex
    octet_length of offset old omit on one only open or order out outer over overlaps overlay
    parameter partition pattern per percent percent_rank percentile_cont percentile_disc period
    portion position position_regex power precedes precision prepare primary procedure ptf range
    rank reads real recursive ref references referencing regr_avgx regr_avgy regr_count
    regr_intercept regr_r2 regr_slope regr_sxx regr_sxy regr_syy release result return returns
    revoke right rollback rollup row row_number rows running savepoint scope scroll search
    second seek select sensitive session_user set show similar sin sinh skip smallint some
    specific specifictype sql sqlexception sqlstate sqlwarning sqrt start static stddev_pop
    stddev_samp submultiset subset substring substring_regex succeeds sum symmetric system
    system_time system_user table tablesample tan tanh then time timestamp timezone_hour
    timezone_minute to trailing translate translate_regex translation treat trigger trim
    trim_array true truncate uescape union unique unknown unnest update upper user using value
    value_of values var_pop var_samp varbinary varchar varying versioning when whenever where
    width_bucket window with within without xml xmlagg xmlattributes xmlbinary xmlcast
    xmlcomment xmlconcat xmldocument xmlelement xmlexists xmlforest xmliterate xmlnamespaces
    xmlparse xmlpi xmlquery xmlserialize xmltable xmltext xmlvalidate year
    """.split())


# end of file
